import { writable, get } from "svelte/store";
import { request } from "~/utils/request";
import { dateFormatting } from "~/utils/date";

export const user_invoice_store = writable({});

export class UserInvoiceHandler {
  static init(user_id, year, month) {
    if (!Object.keys(get(user_invoice_store)).length) {
      console.log("get", get(user_invoice_store));
      UserInvoiceHandler._update(user_id, year, month);
    }
  }

  static _update(user_id, year, month) {
    month = dateFormatting(month);
    return new Promise((resolve, reject) => {
      request(
        `/api/invoice/user?user_id=${user_id}&year=${year}&month=${month}`,
        "get",
        {},
        {},
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          user_invoice_store.set(data);
          resolve();
        }
      });
    });
  }

  static create(user_id, year, month) {
    return new Promise((resolve, reject) => {
      request(
        "/api/invoice/user",
        "post",
        {},
        JSON.stringify({ user_id, year, month }),
        "access"
      ).then(({ status, data }) => {
        if (status == 201) {
          resolve({ status, data });
        }
      });
    });
  }
}
