import { writable, get } from "svelte/store";
import { request } from "~/utils/request";

export let _last_option;
export let transaction_store = writable([]);

export class TransactionHandler {
  static init(lookup_option) {
    if (!get(transaction_store).length) {
      TransactionHandler._update(lookup_option);
    }
    _last_option = { ...lookup_option };
  }

  static _update(lookup_option) {
    let options = { ...lookup_option };
    ["start_date", "end_date", "user_id", "insurance_company_id"].forEach(
      (key_name) => {
        if (
          options.hasOwnProperty(key_name) &&
          (options[key_name] == "" || options[key_name] == -1)
        ) {
          delete options[key_name];
        }
      }
    );
    return new Promise((resolve, reject) => {
      request(
        "/api/transaction/table",
        "post",
        {},
        JSON.stringify(options),
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          transaction_store.set(data);
          resolve();
        }
      });
    });
  }

  static create(transaction) {
    return new Promise((resolve, reject) => {
      request(
        "/api/transaction",
        "post",
        {},
        JSON.stringify(transaction),
        "access"
      ).then(({ status, data }) => {
        if (status == 201) {
          this._update(_last_option).then(() => resolve({ status, data }));
        } else resolve({ status, data });
      });
    });
  }

  static update(id, transaction) {
    return new Promise((resolve, reject) => {
      request(
        `/api/transaction/${id}`,
        "put",
        {},
        JSON.stringify(transaction),
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          this._update(_last_option).then(() => resolve({ status, data }));
        } else resolve({ status, data });
      });
    });
  }

  static delete(id) {
    return new Promise((resolve, reject) => {
      request(`/api/transaction/${id}`, "delete", {}, {}, "access").then(
        ({ status, data }) => {
          if (status == 200) {
            this._update(_last_option).then(() => resolve({ status, data }));
          } else resolve({ status, data });
        }
      );
    });
  }
}
