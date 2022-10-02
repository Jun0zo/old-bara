import { request } from "~/utils/request";

const parse_jwt = (token) => {
  const base64Url = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
};

export const get_userId_from_jwt = (token) => {
  return parseInt(parse_jwt(token).sub);
};

export const get_userInfo_from_id = (id) => {
  return new Promise((resolve, reject) => {
    let seesion_user_info = sessionStorage.getItem("UserItem");
    if (seesion_user_info != null) {
      resolve(seesion_user_info);
    } else {
      request(`/api/user/${id}`, "get", {}, {}, "access").then(
        ({ status, data }) => {
          sessionStorage.setItem("UserInfo", JSON.stringify(data));
          resolve(data.result);
        }
      );
    }
  });
};
