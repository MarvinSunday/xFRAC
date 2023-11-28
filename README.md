# xFRAC
The First Native Fractional NFT Marketplace on the XRP Ledger.
A Sustainable way to Tokenization and Fractionalization On-chain and Real World Assets with the XRP Ledger.

📝Made by @MarvinSunday - Campus Ambassador Falls 2023 Cohorts.

🧑‍💻Code by @ObiajuluM - XRPL Developer

## Table of Content
1. [🌐 Overview](#overview)
2. [💱 xFRAC](#xfrac)
3. [🛠 Our Codes/Libraries](#our-codes/libraries)
4. [🪙rTokens](#rtokens)
5. [📝 Conclusion](#conclusion)
6. [📃 The rPAPER](https://xfrac.gitbook.io/the-rpaper-1/)
<a name="overview"></a>
## Overview 🌐
xFRAC is XRP Ledger’s First Native Fractional NFT Marketplace. This platform helps to increase the liquidity and tradability of XRPL NFTs using a simple Issuer Wallet, AMM, Native XRPL DEX, XLS-20 NFTs, and XRPL Token concepts. The xFRAC platform allows users to change their NFTs into Fractional NFTs to boost the tradability of the NFT Asset on the XRPL through the Native DEX and AMM. xFRAC's concept of fractional NFTs involves converting them into a fungible derivative of the actual NFTs through the rTokenization process. This process allows for the easy forward and backward conversion of NFTs on the xFRAC platform, and this gives birth to an asset category still on the XRPL Token infrastructure earlier stated as rTokens. The final aim of building the infrastructure is to make NFTs highly liquidity and possibly distribute the ownership of NFTs across many XRPL wallets due to the fungible state of rTokens.
<a name= "xfrac"></a>
## xFRAC 💱
To attain a sustainable Tokenization, Fractionalization, Liquidity Provision, and trading of On-chain and Real World assets in the form of Fractional NFT on the Ledger, the xFRAC created the following products. Some of these products are extensions/UIs of XRP Ledger Native Objects, and they help sustain the NFT and fractional ecosystem on the XRPL. They are listed below:
### xFRAC Wallets 👛
xFRAC wallets are XRPL rToken Issuer Wallets that hold NFTs and receive exchange fees on the xFRAC Marketplace.
it is safe to say xFRAC wallets are vaulting and exchanging machines for NFTs as their purpose is to do the following;
1. Receive NFTs and issue the corresponding rTokens.
2. Receive rTokens and release NFTs.
3. Receive Fractioning and De-fractioning exchange fees in XRP, XFC, and rTokens.
This made possible by the current bug fix that allows issuer wallets to exchange Tokens and NFT with thier issued currency.
### xFRADEX 💱
xFRADEX is a UI of the XRP Ledger Native DEX tailored toward trading rTokens on xFRAC. This DEX interface saves the xFRAC Team from having to list each rToken on other DEXs, as users can easily buy or sell their rTokens on the DEX. 
### xFRAPOOL 💱
xFRAPOOL is a UI of the XRP Ledger Native Automatic Market Maker Liquidity provision and Swap function.
With the Fractional NFT version we are using (IOU Tokens), it will be impossible to maintain a stable price of the Fractional NFTs without an AMM function. The integration of XRP Ledger Native AMM helps our Fractional NFTs (rTokens) to remain stable and liquid.
xFRAPOOL saves xFRAC Users the time of adding/removing Liquidity and Swapping through a raw transaction function or seeking for XRPL DEXs that support rToken LP Pools.
### rToken Governance & xFAC DAO 🗳️
xFRAC DAO is the body of rToken Holders, rToken LP Holders, and our Utility Token holders. They Govern the platform through an On-chain Governance mechanism called the rToken Governance Process. They vote and raise proposals on matters of our utility Token, rTokens, and the Governance Process.
We are integrating Rippled scripts and APIs that track votes and compute the results from the Governance Process in real time. 
<a name="our-codes/libraries"></a>
## Our Codes/Libraries 🛠️
Our Codes are in Python and JavaScript programming languages. We used existing XRPL libraries like xumm js SDK and xrpl-py SDK. Our platform allows XUMM and Crossmark Plugin.
Our platform interacts with the following XRP Ledger objects. Token Trustlines (Token issuance and Token account setting), Native Order DEX (for creating Token-Token offers), XLS-20 NFTokens (for creating Token-NFT offers and NFT issuing), XLS-30D Native Token AMM (to create AMMs, Swap from an AMM, and Add Liquidity to an AMM), XLS-39D Token Clawback (used in our real-world applications of xFRAC technology), and signerList function on our utility Token reward Vault/wallet.
<a name="rtokens"></a>
## rTokens 🪙
rTokens are 1:1 IOU Tokens representing each NFT locked in the fractional NFT Vault (xFRAC Wallets). They are the fungible version of every NFT locked in an xFRAC wallet. They make the following to be possible:
1. With rTokens, NFTs are owned by multiple XRPL Wallets.
2. They increase the liquidity and tradability of NFTs via the XRPL Native Order Book DEX and AMM.
3. They allow for easy NFT redemption from xFRAC wallets, as each unit of a rToken represents an NFT.
<a name="conclusion"></a>
## Conclusion 📝
