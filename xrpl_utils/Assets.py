
from xrpl.models import (AccountSet, AccountSetFlag, IssuedCurrencyAmount,
                         NFTokenBurn, NFTokenMint, NFTokenMintFlag, Payment,
                         TrustSet, Transaction, AccountSetAsfFlag)
from xrpl.clients.json_rpc_client import JsonRpcClient
from xrpl.transaction.main  import autofill_and_sign, sign_and_submit
from xrpl.wallet import Wallet

from Misc import (mm, nft_fee_to_xrp_format,
                  transfer_fee_to_xrp_format, validate_symbol_to_hex)
from x_constants import M_SOURCE_TAG

"""create tokens, nfts"""


"""steps to creating a token; must use 2 new accounts"""
"""1"""
def accountset_issuer(issuer_addr: str, ticksize: int, transferfee: float, domain: str, fee: str = None) -> dict:
    txn = AccountSet(account=issuer_addr, set_flag=AccountSetAsfFlag.ASF_DEFAULT_RIPPLE, tick_size=ticksize,
    transfer_rate=transfer_fee_to_xrp_format(transferfee), domain=validate_symbol_to_hex(domain), fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()

"""2"""
def accountset_manager(manager_addr: str, domain: str, fee: str = None) -> dict:
    txn = AccountSet(account=manager_addr,
                        set_flag=AccountSetAsfFlag.ASF_REQUIRE_AUTH, # TF_REQUIRE_AUTH
                    domain=validate_symbol_to_hex(domain), fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()

"""3"""
def create_trustline(manager_addr: str, issuer_addr: str, token_name: str, total_supply: str, fee: str = None) -> dict:
    txn = TrustSet(
        account=manager_addr,
        limit_amount=IssuedCurrencyAmount(
            currency=validate_symbol_to_hex(token_name),
            issuer=issuer_addr,
            value=total_supply,
        ),source_tag=M_SOURCE_TAG,
        # flags=TrustSetFlag.TF_SET_NO_RIPPLE,
            fee=fee, memos=mm())
    return txn.to_xrpl()

"""4"""
def create_token(issuer_addr: str, manager_addr: str, token_name: str, total_supply: str, fee: str = None) -> dict:
    txn = Payment(
        account=issuer_addr,
        destination=manager_addr,
        amount=IssuedCurrencyAmount(
            currency=validate_symbol_to_hex(token_name),
            issuer=issuer_addr,
            value=total_supply), fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()

def burn_token(sender_addr: str, token: str, issuer: str, amount: float, fee: str = None) -> dict:
    """burn a token"""
    txn = Payment(
        account=sender_addr,
        destination=issuer,
        amount=IssuedCurrencyAmount(currency=validate_symbol_to_hex(token), issuer=issuer, value=amount), fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()

def mint_nft(issuer_addr: str, taxon: int, is_transferable: bool, only_xrp: bool, issuer_burn: bool, transfer_fee: float = None, uri: str = None, fee: str = None) -> dict:
    """mint nft"""
    flag = []
    if is_transferable:
        flag.append(NFTokenMintFlag.TF_TRANSFERABLE) # nft can be transferred
    if only_xrp:
        flag.append(NFTokenMintFlag.TF_ONLY_XRP) # nft may be traded for xrp only
    if issuer_burn:
        flag.append(NFTokenMintFlag.TF_BURNABLE) # If set, indicates that the minted token may be burned by the issuer even if the issuer does not currently hold the token.
    txn = NFTokenMint(
        account=issuer_addr,
        nftoken_taxon=taxon,
        uri=validate_symbol_to_hex(uri), flags=flag, transfer_fee=nft_fee_to_xrp_format(transfer_fee), fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()

def burn_nft(sender_addr: str, nftoken_id: str, holder: str = None, fee: str = None) -> dict:
    """burn an nft, specify the holder if the token is not in your wallet, only issuer and holder can call"""
    txn = NFTokenBurn(account=sender_addr, nftoken_id=nftoken_id, owner=holder, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()




# token_client = JsonRpcClient("http://s.devnet.rippletest.net:51234")
# issuer1 = Wallet.from_seed(seed= "sEdS1jTVU58HsPeL4xhPkziphnxFDHz") # rHTfx7p4ge8CfDhyoczpSwc84LWfiK3dhN


# manager1 = Wallet.from_seed(seed= "sEdVdthdYnRRLqBXAD76QC7CatoLqU8")
# print(manager1.classic_address) # rBoSibkbwaAUEpkehYixQrXp4AqZez9WqA
# token1 = "NGN"





# one = accountset_issuer(
#     issuer_addr= issuer1.classic_address,
#     ticksize= 3,
#     transferfee=0,
#     domain = "ngn.com"
# )

# print(sign_and_submit(
# Transaction.from_xrpl(
#     one
# ),token_client, issuer1, ))


# two = accountset_manager(
#     manager1.classic_address,
#     "ngn.com",
# )

# print(sign_and_submit(
# Transaction.from_xrpl(
#     two
# ),token_client, manager1, ))

# three = create_trustline(
#     manager_addr=manager1.classic_address,
#     issuer_addr=issuer1.classic_address,
#     token_name=token1,
#     total_supply="100000000000"
# )

# print(sign_and_submit(
# Transaction.from_xrpl(
#     three
# ),token_client, manager1, ))

# four = create_token(
#     issuer_addr=issuer1.classic_address,
#     manager_addr=manager1.classic_address,
#     token_name=token1,
#     total_supply="100000000000"
# )

# print(sign_and_submit(
# Transaction.from_xrpl(
#     four
# ),token_client, issuer1, ))






