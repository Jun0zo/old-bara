import { writable, get } from "svelte/store";
import { request } from "~/utils/request";
import { dateFormatting } from "~/utils/date";

import { UserInvoiceHandler } from "~/data/Invoice/UserInvoice";

export let user_extra_store = writable([]);

export class UserExtraHandler {
  static init(user_id, year, month) {
    if (!get(user_extra_store).length) {
      UserExtraHandler._update(user_id, year, month);
    }
  }

  static _update(user_id, year, month) {
    month = dateFormatting(month);
    return new Promise((resolve, reject) => {
      request(
        `api/invoice/user/extra?user_id=${user_id}&year=${year}&month=${month}`,
        "get",
        {},
        {},
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          user_extra_store.set(data);
          resolve();
        }
      });
    });
  }

  static update(user_id, year, month, extra_info) {
    return new Promise((resolve, reject) => {
      request(
        `api/invoice/user/extra/${extra_info.id}`,
        "put",
        {},
        JSON.stringify({ name: extra_info.name, price: extra_info.price }),
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          this._update(user_id, year, month);
          UserInvoiceHandler._update(user_id, year, month);
        }
        resolve({ status, data });
      });
    });
  }

  static create(user_id, year, month, extra_name, price) {
    return new Promise((resolve, reject) => {
      request(
        `api/invoice/user/extra`,
        "post",
        {},
        JSON.stringify({ user_id, year, month, name: extra_name, price }),
        "access"
      ).then(({ status, data }) => {
        if (status == 201) {
          this._update(user_id, year, month);
          UserInvoiceHandler._update(user_id, year, month);
        }
        resolve({ status, data });
      });
    });
  }

  static delete(user_id, year, month, extra_id) {
    return new Promise((resolve, reject) => {
      request(
        `api/invoice/user/extra/${extra_id}`,
        "delete",
        {},
        {},
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          this._update(user_id, year, month);
          UserInvoiceHandler._update(user_id, year, month);
        }
        resolve({ status, data });
      });
    });
  }
}
