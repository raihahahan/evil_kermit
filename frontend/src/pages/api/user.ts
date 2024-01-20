import { NextApiRequest, NextApiResponse } from "next";
import { APP_SETTINGS } from "../../common/appSettings";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

    if (req.method == "POST") {
      const action = req.query?.action;
      if (action == "start") {
        const bodyData = JSON.parse(req.body);
        const username = bodyData?.username ?? "";
        const phone = bodyData?.phone ?? "";
        const whitelist = bodyData?.whitelist ?? [];
        console.log(whitelist);
        await fetch(
          `${APP_SETTINGS.BACKEND_URL}/user/startUser?username=${username}&phone=${phone}`,
          {
            method: "POST",
            body: JSON.stringify(whitelist),
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          }
        );
      } else if (action == "confirm") {
        const bodyData = JSON.parse(req.body);
        const username = bodyData?.username ?? "";
        const passcode = bodyData?.passcode ?? "";

        await fetch(
          `${APP_SETTINGS.BACKEND_URL}/user/confirmPasscode?username=${username}&passcode=${passcode}`,
          {
            method: "POST",
          }
        );
      } else if (action == "stop") {
        const bodyData = JSON.parse(req.body);
        const username = bodyData?.username ?? "";

        await fetch(
          `${APP_SETTINGS.BACKEND_URL}/user/stopClient?username=${username}`,
          {
            method: "POST",
          }
        );
      }

      res.status(200).json({ message: "Ok" });
    }
  } catch (e) {
    console.log(e);
  }
}
