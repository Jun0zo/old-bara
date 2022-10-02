export const request = (
  url,
  method = "get",
  headers = { },
  body = {},
  auth = "none"
) => {
  headers['accept'] = "application/json";
  headers['Content-Type'] = "application/json";
  if (auth == "access") {
    headers["accept"] = "application/json";
    headers["Authorization"] = `Bearer ${localStorage.getItem("access_token")}`;
  } else if (auth == "refresh") {
    headers["accept"] = "application/json";
    headers["Authorization"] = `Bearer ${localStorage.getItem(
      "refresh_token"
    )}`;
  }

  let option = {
    method: method,
    headers: headers,
  };
  let status = 0;
  let data = {};
  if (method != "get" && method != "haed") {
    option["body"] = body;
    console.log(option["body"]);
  }
  return new Promise((resolve, reject) => {
    fetch(url, option)
      .then((res) => {
        status = res.status;
        return res.json();
      })
      .then((res) => {
        data = res;
        resolve({ status, data });
      });
  }).catch((e) => {
    console.log("in error", e);
  });
};


