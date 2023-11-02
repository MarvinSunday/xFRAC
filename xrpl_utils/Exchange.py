import asyncio
from typing import Union

from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.models import (XRP, AccountOffers, AMMCreate, AMMVote, BookOffers,
                         IssuedCurrency, IssuedCurrencyAmount, OfferCreate,
                         OfferCreateFlag, AuthAccount, AMMBid, OfferCancel)
from xrpl.utils import drops_to_xrp, xrp_to_drops

from Misc import (amm_fee_to_xrp_format, mm,
                  validate_hex_to_symbol)
from Objects import xObject
from x_constants import M_SOURCE_TAG

"""
Swap objects

Manages AMM and order book objects

Call order book swaps Non determinstic swap (sounds cool)
"""

class xOrderBook(AsyncJsonRpcClient):
    def __init__(self, url: str):
        self.client = AsyncJsonRpcClient(url) 

    async def get_account_order_book_liquidity(self, wallet_addr: str) -> list:
        """return all offers that are liquidity an account created"""
        offer_list = []

        req = AccountOffers(account=wallet_addr, ledger_index="validated")
        response = await self.client.request(req)
        result = response.result
        if "offers" in result:
            offers = result["offers"]
            for offer in offers:
                if 0x00010000 & offer["flags"] == 0x00010000:
                    of = {}
                    of["flags"] = offer["flags"]
                    of["sequence"] = offer["seq"]
                    of["quality"] = offer["quality"]# str(drops_to_xrp(offer["quality"])) # rate is subject to error from the blockchain because xrp returned in this call has no decimal  # The exchange rate of the offer, as the ratio of the original taker_pays divided by the original taker_gets. rate = pay/get
                    if isinstance(offer["taker_pays"], dict):
                        of["buy_token"] = validate_hex_to_symbol(offer["taker_pays"]["currency"])
                        of["buy_issuer"] = offer["taker_pays"]["issuer"]
                        of["buy_amount"] = offer["taker_pays"]["value"]
                    elif isinstance(offer["taker_pays"], str):
                        of["buy_token"] = "XRP"
                        of["buy_issuer"] = ""
                        of["buy_amount"] = str(drops_to_xrp(offer["taker_pays"]))
                    if isinstance(offer["taker_gets"], dict):
                        of["sell_token"] = validate_hex_to_symbol(offer["taker_gets"]["currency"])
                        of["sell_issuer"] = offer["taker_gets"]["issuer"]
                        of["sell_amount"] = offer["taker_gets"]["value"]
                    elif isinstance(offer["taker_gets"], str):
                        of["sell_token"] = "XRP"
                        of["sell_issuer"] = ""
                        of["sell_amount"] = str(drops_to_xrp(offer["taker_gets"]))
                    of["rate"] = float(of["sell_amount"])/float(of["buy_amount"])
                    offer_list.append(of)
        return offer_list
        
    async def sort_best_offer(self, buy: Union[XRP, IssuedCurrency], sell: Union[XRP, IssuedCurrency], best_buy: bool = False, best_sell: bool = False) -> dict:
        """return all available orders and best {option} first, choose either best_buy or best_sell"""
        best = {}

        if best_sell:
            req = BookOffers(taker_gets=sell, taker_pays=buy, ledger_index="validated")
            response = await self.client.request(req)
            result = response.result
            if "offers" in result:
                offers: list = result["offers"]
                # sort offer list and return highest rate first
                offers.sort(key=lambda object: object["quality"], reverse=True)
                index = 0
                for offer in offers:
                    of = {}
                    of["creator"] = offer["Account"]
                    of["offer_id"] = offer["index"]
                    of["flags"] = offer["Flags"]
                    of["sequence"] = offer["Sequence"] # offer id
                    of["rate"] = offer["quality"]
                    of["creator_liquidity"] = ""
                    if "owner_funds" in offer:
                        of["creator_liquidity"] = offer["owner_funds"] # available amount the offer creator of `sell_token` is currently holding
                    if isinstance(offer["TakerPays"], dict):
                        of["buy_token"] = validate_hex_to_symbol(offer["TakerPays"]["currency"])
                        of["buy_issuer"] = offer["TakerPays"]["issuer"]
                        of["buy_amount"] = offer["TakerPays"]["value"]
                    elif isinstance(offer["TakerPays"], str):
                        of["buy_token"] = "XRP"
                        of["buy_issuer"] = ""
                        of["buy_amount"] = str(drops_to_xrp(offer["TakerPays"]))

                    if isinstance(offer["TakerGets"], dict):
                        of["sell_token"] = validate_hex_to_symbol(offer["TakerGets"]["currency"])
                        of["sell_issuer"] = offer["TakerGets"]["issuer"]
                        of["sell_amount"] = offer["TakerGets"]["value"]
                    elif isinstance(offer["TakerGets"], str):
                        of["sell_token"] = "XRP"
                        of["sell_issuer"] = ""
                        of["sell_amount"] = str(drops_to_xrp(offer["TakerGets"]))                    
                    index += 1
                    best[index] = of

        if best_buy:
            req = BookOffers(taker_gets=sell, taker_pays=buy, ledger_index="validated")
            response = await self.client.request(req)
            result = response.result
            if "offers" in result:
                offers: list = result["offers"]
                # sort offer list and return lowest rate first
                offers.sort(key=lambda object: object["quality"])
                index = 0
                for offer in offers:
                    of = {}
                    of["creator"] = offer["Account"]
                    of["offer_id"] = offer["index"]
                    of["flags"] = offer["Flags"]
                    of["sequence"] = offer["Sequence"] # offer id
                    of["rate"] = offer["quality"]
                    of["creator_liquidity"] = ""
                    if "owner_funds" in offer:
                        of["creator_liquidity"] = offer["owner_funds"] # available amount the offer creator is currently holding
                    if isinstance(offer["TakerPays"], dict):
                        of["buy_token"] = validate_hex_to_symbol(offer["TakerPays"]["currency"])
                        of["buy_issuer"] = offer["TakerPays"]["issuer"]
                        of["buy_amount"] = offer["TakerPays"]["value"]
                    elif isinstance(offer["TakerPays"], str):
                        of["buy_token"] = "XRP"
                        of["buy_issuer"] = ""
                        of["buy_amount"] = str(drops_to_xrp(offer["TakerPays"]))

                    if isinstance(offer["TakerGets"], dict):
                        of["sell_token"] = validate_hex_to_symbol(offer["TakerGets"]["currency"])
                        of["sell_issuer"] = offer["TakerGets"]["issuer"]
                        of["sell_amount"] = offer["TakerGets"]["value"]
                    elif isinstance(offer["TakerGets"], str):
                        of["sell_token"] = "XRP"
                        of["sell_issuer"] = ""
                        of["sell_amount"] = str(drops_to_xrp(offer["TakerGets"]))                    
                    index += 1
                    best[index] = of
        return best

def cancel_offer(sender_addr: str, offer_seq: int, fee: str = None) -> dict:
    """cancel an offer"""
    txn = OfferCancel(account=sender_addr, offer_sequence=offer_seq, fee=fee, memos=mm, source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()

def create_order_book_liquidity(sender_addr: str, buy: Union[float, IssuedCurrencyAmount], sell: Union[float, IssuedCurrencyAmount], expiry_date: int = None, fee: str = None) -> dict:
    """create an offer as passive; it doesn't immediately consume offers that match it, just stays on the ledger as an object for liquidity"""
    flags = [OfferCreateFlag.TF_PASSIVE]
    tx_dict = {}
    if isinstance(buy, float) and isinstance(sell, IssuedCurrencyAmount): # check if give == xrp and get == asset
        txn = OfferCreate(account=sender_addr, taker_pays=xrp_to_drops(buy), taker_gets=sell, flags=flags, expiration=expiry_date, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
        tx_dict = txn.to_xrpl()
    if isinstance(buy, IssuedCurrencyAmount) and isinstance(sell, float): # check if give == asset and get == xrp
        txn = OfferCreate(account=sender_addr, taker_pays=buy, taker_gets=xrp_to_drops(sell), flags=flags, expiration=expiry_date, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
        tx_dict = txn.to_xrpl()
    if isinstance(buy, IssuedCurrencyAmount) and isinstance(sell, IssuedCurrencyAmount): # check if give and get are == asset
        txn = OfferCreate(account=sender_addr, taker_pays=buy, taker_gets=sell, flags=flags, expiration=expiry_date, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
        tx_dict = txn.to_xrpl()
    return tx_dict

def order_book_swap(sender_addr: str, buy: Union[float, IssuedCurrencyAmount], sell: Union[float, IssuedCurrencyAmount], tf_sell: bool = False, tf_fill_or_kill: bool = False, tf_immediate_or_cancel: bool = False, fee: str = None) -> dict:
    """create an offer that either matches with existing offers to get entire sell amount or cancels\n
    if swap_all is enabled, this will force exchange all the paying units regardless of profit or loss\n

    if tecKILLED is the result, exchange didnt go through because all of the `buy` couldnt be obtained. recommend enabling swap_all
    """
    flags = []
    if tf_sell:
        flags.append(OfferCreateFlag.TF_SELL)
    if tf_fill_or_kill:
        flags.append(OfferCreateFlag.TF_FILL_OR_KILL)
    if tf_immediate_or_cancel:
        flags.append(OfferCreateFlag.TF_IMMEDIATE_OR_CANCEL)
    tx_dict = {}
    if isinstance(buy, float) and isinstance(sell, IssuedCurrencyAmount): # check if give == xrp and get == asset
        txn = OfferCreate(account=sender_addr, taker_pays=xrp_to_drops(buy), taker_gets=sell, flags=flags, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
        tx_dict = txn.to_xrpl()
    if isinstance(buy, IssuedCurrencyAmount) and isinstance(sell, float): # check if give == asset and get == xrp
        txn = OfferCreate(account=sender_addr, taker_pays=buy, taker_gets=xrp_to_drops(sell), flags=flags, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
        tx_dict = txn.to_xrpl()
    if isinstance(buy, IssuedCurrencyAmount) and isinstance(sell, IssuedCurrencyAmount): # check if give and get are == asset
        txn = OfferCreate(account=sender_addr, taker_pays=buy, taker_gets=sell, flags=flags, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
        tx_dict = txn.to_xrpl()
    return tx_dict









"""The AMM ERA is here"""

"""Liquidity providers can vote to set the fee from 0% to 1%, in increments of 0.%."""
def create_amm(sender_addr: str, token_1: Union[float, IssuedCurrencyAmount], token_2: Union[float, IssuedCurrencyAmount], trading_fee: float, fee: str = None) -> dict:
    """create a liquidity pool for asset pairs if one doesnt already exist"""      
    token1 = xrp_to_drops(token_1) if isinstance(token_1, float) else token_1
    token2 = xrp_to_drops(token_2) if isinstance(token_2, float) else token_2
    txn = AMMCreate(
        account=sender_addr,
        amount=token1,
        amount2=token2,
        trading_fee=amm_fee_to_xrp_format(trading_fee), fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl() 

def amm_vote( sender_addr: str, token_1: Union[XRP, IssuedCurrency], token_2: Union[XRP, IssuedCurrency], trading_fee: float, fee: str = None) -> dict:
    """cast a vote to modify AMM fee"""
    txn = AMMVote(
        account=sender_addr,
        asset=token_1,
        asset2=token_2,
        trading_fee=amm_fee_to_xrp_format(trading_fee), fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl() 


"""work this"""
def amm_bid( sender_addr: str, token_1: Union[XRP, IssuedCurrency], token_2: Union[XRP, IssuedCurrency],
    auth_accounts: list[AuthAccount] = None, bid_max: IssuedCurrencyAmount= None, bid_min: IssuedCurrencyAmount = None, fee: str = None):
    """token 1 and 2 are the amm tokens, bid max and bid min are the Lp's token"""
    txn = AMMBid(
        account=sender_addr,
        asset=token_1,
        asset2=token_2,
        auth_accounts=auth_accounts,
        bid_max=bid_max,
        bid_min=bid_min, source_tag=M_SOURCE_TAG)
    return txn.to_xrpl() 
