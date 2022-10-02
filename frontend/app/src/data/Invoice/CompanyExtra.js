import { writable, get } from "svelte/store";
import { request } from "~/utils/request";
import { dateFormatting } from "~/utils/date";

export let company_extra_store = writable([]);

export class CompanyExtraHandler {
  static init(year, month) {
    if (!get(company_extra_store).length) {
      CompanyExtraHandler._update(year, month);
    }
  }

  static _update(year, month) {
    month = dateFormatting(month);
    return new Promise((resolve, reject) => {
      request(
        `api/invoice/company/extra?year=${year}&month=${month}`,
        "get",
        {},
        {},
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          company_extra_store.set(data);
          resolve();
        }
      });
    });
  }

  static update(extra_id) {
    return new Promise((resolve, reject) => {
      request(
        `api/invoice/company/extra/${extra_id}`,
        "put",
        {},
        {},
        "access"
      ).then(({ status, data }) => {
        if (status == 200) {
          alert("정상적으로 수정되었습니다!");
          if (status == 200)
            this._update().then(() => resolve({ status, data }));
          resolve({ status, data });
        }
      });
    });
  }

  static delete(user_id) {
    return new Promise((resolve, reject) => {
      request(`/api/user/${user_id}`, "delete", {}, {}, "access").then(
        ({ status, data }) => {
          if (status == 200)
            this._update().then(() => resolve({ status, data }));
          resolve({ status, data });
        }
      );
    });
  }
}
