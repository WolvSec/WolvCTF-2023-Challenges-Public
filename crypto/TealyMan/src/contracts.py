from pyteal import *


def approval_program():
    ctf_admin_key = Bytes("admin_key")
    seller_key = Bytes("seller")
    nft_id_key = Bytes("nft_id")
    start_time_key = Bytes("start")
    end_time_key = Bytes("end")

    @Subroutine(TealType.none)
    def decrementNFTTo(assetID: Expr, account: Expr) -> Expr:
        asset_holding = AssetHolding.balance(
            Global.current_application_address(), assetID
        )
        return Seq(
            asset_holding,
            If(asset_holding.hasValue()).Then(
                Seq(
                    InnerTxnBuilder.Begin(),
                    InnerTxnBuilder.SetFields(
                        {
                            TxnField.type_enum: TxnType.AssetTransfer,
                            TxnField.xfer_asset: assetID,
                            TxnField.asset_close_to: account,
                        }
                    ),
                    InnerTxnBuilder.Submit(),
                )
            ),
        )

    @Subroutine(TealType.none)
    def closeAccountTo(account: Expr) -> Expr:
        return If(Balance(Global.current_application_address()) != Int(0)).Then(
            Seq(
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.Payment,
                        TxnField.close_remainder_to: account,
                    }
                ),
                InnerTxnBuilder.Submit(),
            )
        )
    
    @Subroutine(TealType.uint64)
    def isLessThan(left, right) -> Expr:
        return Seq(
            If(And(Int(0x8000000000000000) & left)).Then(
                If(And(Int(0x8000000000000000) & right)).Then(
                    If(left > right).Then(
                        Return(Int(1))
                    ).Else(
                        Return(Int(0))
                    )
                ).Else(
                    Return(Int(1))
                )
            ).Else(
                If(And(Int(0x8000000000000000) & right)).Then(
                    Return(Int(0))
                ).Else(
                    If(left < right).Then(
                        Return(Int(1))
                    ).Else(
                        Return(Int(0))
                    )
                )
            )
        )

    on_setup = Seq(
        # opt into NFT asset -- because you can't opt in if you're already opted in, this is what
        # we'll use to make sure the contract has been set up
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Txn.assets[0],
                TxnField.asset_receiver: Global.current_application_address(),
            }
        ),
        InnerTxnBuilder.Submit(),
        App.localPut(Txn.sender(), nft_id_key, Txn.assets[0]),
        App.localPut(Txn.sender(), seller_key, Txn.sender()),
        App.localPut(Txn.sender(), start_time_key, Global.latest_timestamp() ),
        App.localPut(Txn.sender(), end_time_key, Btoi(Txn.application_args[1])),
        Assert(
            And(
                App.localGet(Txn.sender(), start_time_key) < App.localGet(Txn.sender(), end_time_key),
            )
        ),
        Approve(),
    )

    on_bid_txn_index = Txn.group_index() - Int(1)
    on_bid_nft_holding = AssetHolding.balance(
        Global.current_application_address(), Txn.assets[0]
    )
    on_purchase = Seq(
        on_bid_nft_holding,
        Assert(
            And(
                # the auction has been set up
                on_bid_nft_holding.hasValue(),
                isLessThan(Int(0), on_bid_nft_holding.value()),
                # # the auction has started
                isLessThan(App.localGet(Txn.sender(), start_time_key), Global.latest_timestamp()),
                # # the auction has not ended
                isLessThan(Global.latest_timestamp(), App.localGet(Txn.sender(), end_time_key)),
                # the actual bid payment is before the app call
                Gtxn[on_bid_txn_index].type_enum() == TxnType.Payment,
                Gtxn[on_bid_txn_index].sender() == Txn.sender(),
                Gtxn[on_bid_txn_index].receiver()
                == Global.current_application_address(),
                isLessThan(Global.min_txn_fee(), Gtxn[on_bid_txn_index].amount())
            )
        ),
        If(
            isLessThan(Btoi(Txn.application_args[1]) + Global.latest_timestamp(), App.localGet(Txn.sender(), start_time_key))
        ).Then(
            Seq(
                decrementNFTTo(
                    # TODO: set some local storage to a signed flag encrypted with the seller's address
                    App.localGet(Txn.sender(), nft_id_key),
                    Txn.sender(),
                ),
                Approve(),
            )
        ).Else(
            Reject(),
        )
    )

    on_call = Cond(
        [Txn.application_args[0] == Bytes("setup"), on_setup],
        [Txn.application_args[0] == Bytes("buy"), on_purchase]
    )       

    on_delete = Seq(
        Assert(
            Txn.sender() == Global.creator_address()
        ),
        closeAccountTo(App.globalGet(ctf_admin_key)),
        Approve()
    )

    program = Cond(
        [
            Txn.application_id() == Int(0), 
            Seq(
                App.globalPut(ctf_admin_key, Txn.sender()),
                Approve()
            )
        ],
        [Txn.on_completion() == OnComplete.NoOp, on_call],
        [Txn.on_completion() == OnComplete.OptIn, Approve()],
        [Txn.on_completion() == OnComplete.CloseOut, Approve()],
        [
            Txn.on_completion() == OnComplete.DeleteApplication,
            on_delete,
        ],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()]
    )

    with open("build/auction.teal", "w+") as f:
        f.write(compileTeal(program, Mode.Application, version=5))

def clear_state_program():
    with open("build/clear.teal", "w+") as f:
        f.write(compileTeal(Approve(), Mode.Application, version=5))


if __name__ == "__main__":
    approval_program()
    clear_state_program()
