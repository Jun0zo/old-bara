import { writable, get } from "svelte/store";
import { request } from "~/utils/request";

export let employee_store = writable([]);

export class EmployeeHandler {
  static init() {
    if (!get(employee_store).length) {
      EmployeeHandler._update();
    }
  }

  static _update() {
    return new Promise((resolve, reject) => {
      request("/api/user", "get", {}, {}, "access").then(({ status, data }) => {
        if (status == 200) {
          employee_store.set(data);
          resolve();
        }
      });
    });
  }

  static put(target_id) {
    return new Promise((resolve, reject) => {
      request(`/api/user/${target_id}`, "put", {}, {}, "access").then(
        ({ status, data }) => {
          if (status == 200) {
            alert("정상적으로 삭제되었습니다!");
            if (status == 200)
              this._update().then(() => resolve({ status, data }));
            resolve({ status, data });
          }
        }
      );
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

  // Setting
  static accept(new_user_id, new_user_info) {
    return new Promise((resolve, reject) => {
      request(
        `/api/user/${new_user_id}`,
        "put",
        {},
        JSON.stringify(new_user_info),
        "access"
      ).then(({ status, data }) => {
        if (status == 200) this._update().then(() => resolve({ status, data }));
        resolve({ status, data });
      });
    });
  }

  static reject(target_id) {
    return new Promise((resolve, reject) => {
      request(`/api/user/${target_id}`, "delete", {}, {}, "access").then(
        ({ status, data }) => {
          if (status == 200) {
            alert("정상적으로 삭제되었습니다!");
            if (status == 200)
              this._update().then(() => resolve({ status, data }));
            resolve({ status, data });
          }
        }
      );
    });
  }
}

/*
    if (status == 200) {
        alert("정상적으로 등록되었습니다!");
        request_update_role();
        
      } else if (status == 400) {
        //  요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
        alert(data.message);
      } else if (status == 401) {
        //  Token이 유효하지 않은 경우
      } else if (status == 403) {
        //	Token이 없거나 권한이 부족한 경우
      } else if (status == 409) {
        //  DB, 메일 전송 오류 등 예상치 못한 오류가 발생한 경우
      } else if (status == 422) {
        //	요청 파라미터가 유효하지 않은 경우
      }
    */
