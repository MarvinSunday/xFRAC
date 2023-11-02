export const checkForCrossmark = () => {
  try {
    const detect = window.xrpl.isCrossmark;
    return detect;
  } catch (err) {
    console.log(err);
    return err;
  }
};

export const signIn = async () => {
  try {
    checkForCrossmark();
    const sdk = window.xrpl.crossmark;
    let { response } = await sdk.signInAndWait();
    if (response.data.meta.isRejected) {
      console.log("You have to sign in to continue");
      return "You have to sign in to continue";
    }
    if (response.data.meta.isError) {
      console.log("Error encountered during signing");
      return "Error encountered during signing";
    }
    if (response.data.meta.isFailed) {
      console.log("Transaction Failed");
      return "Transaction Failed";
    }
    if (response.data.meta.isExpired) {
      console.log("Transaction Expired");
      return "Transaction Expired";
    }
    let network = response.data.network.type === "test" ? "TESTNET" : "MAINNET";
    let address = response.data.address;
    if (response.data.meta.isSuccess) {
      return { address, network, connected: true };
    }
  } catch (e) {
    console.log(e);
    return e;
  }
};

export const submitTxn = async (TxnReq) => {
  try {
    const sdk = window.xrpl.crossmark;
    let { response } = await sdk.signAndSubmitAndWait(TxnReq);
    if (response.data.meta.isRejected) {
      console.log("Transaction Rejected");
      return "Transaction Rejected";
    }
    if (response.data.meta.isError) {
      console.log("Error encountered during signing");
      return "Error encountered during signing";
    }
    if (response.data.meta.isFail) {
      console.log("Transaction Failed");
      return "Transaction Failed";
    }
    if (response.data.meta.isExpired) {
      console.log("Transaction Expired");
      return "Transaction Expired";
    }
    if (response.data.meta.isSuccess) {
      console.log({ status: "SUCCESS", hash: response.data.resp.result.hash });
      return { status: "SUCCESS", hash: response.data.resp.result.hash };
    }
  } catch (e) {
    console.log(e);
    return e;
  }
};

export const eventHandler = () => {
  try {
    setTimeout(async () => {
      if (checkForCrossmark() === true) {
        let sdk = window.xrpl.crossmark;

        sdk.on("user-change", () => {
          try {
            let address = sdk.session.address;
            let resp = {
              address,
              network:
                sdk.session.network.type === "test" ? "TESTNET" : "MAINNET",
              connected: address ? true : false,
            };
            console.log("userchange");
            console.log(resp);
            return resp;
          } catch (e) {
            console.log(e);
            return e;
          }
        });
        sdk.on("network-change", (res) => {
          try {
            let address = sdk.session.address;
            let resp = {
              address,
              network: res.network.type === "test" ? "TESTNET" : "MAINNET",
              connected: address ? true : false,
            };
            console.log("netchange");
            console.log(resp);
            return resp;
          } catch (e) {
            console.log(e);
            return e;
          }
        });
      }
    }, 5000);
  } catch (e) {
    console.log(e);
    return e;
  }
};
