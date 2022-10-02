<script>
  import Dialog, { Title, Content, Actions, Header } from "@smui/dialog";
  import Textfield from "@smui/textfield";
  import Select, { Option } from "@smui/select";
  import Button, { Label } from "@smui/button";
  import IconButton from "@smui/icon-button";
  import dayjs from "dayjs";

  import { TransactionHandler, transaction_store } from "~/data/Transaction";
  import { EmployeeHandler, employee_store } from "~/data/Employee";
  import {
    InsuranceCompanyHandler,
    insurance_company_store,
  } from "~/data/InsuranceCompany";
  import { Datepicker } from "svelte-calendar";

  import { calendar_theme, locale } from "~/data/date_picker_settings";

  export let open;
  export let target_transaction;
  export let new_transaction;

  let tmp_transaction = {};
  let before_modal_status = false;

  let employee_list = [];
  let insurance_company_list = [];

  let date_store;

  EmployeeHandler.init();
  employee_store.subscribe((value) => {
    if (value.result) employee_list = value.result;
  });

  InsuranceCompanyHandler.init();
  insurance_company_store.subscribe((value) => {
    if (value.result) insurance_company_list = value.result;
  });

  const initModal = () => {
    tmp_transaction = {
      ...target_transaction,
    };
    if (!new_transaction) {
      // 기존 트랜젝션일 경우 모달에 초기값 정보 입력
      let target_company = insurance_company_list.filter(
        (company) =>
          tmp_transaction["insurance_company_name"] == company["name"]
      )[0];
      tmp_transaction["insurance_company_id"] = target_company["id"];

      let target_employee = employee_list.filter(
        (employee) => tmp_transaction["user_name"] == employee["name"]
      )[0];
      tmp_transaction["user_id"] = target_employee["id"];
    }
  };

  $: {
    if (open == true) {
      if (before_modal_status == false) {
        // 모달창 처음 열었을 때
        initModal();
      }
      before_modal_status = true;
    } else {
      tmp_transaction = { ...target_transaction };
      before_modal_status = false;
    }
    console.log(tmp_transaction, tmp_transaction["date"]);
  }

  $: {
    if ($date_store?.hasChosen) {
      tmp_transaction["date"] = dayjs($date_store.selected).format(
        "YYYY-MM-DD"
      );
    } else {
    }
  }

  const create_transaction = (transaction) => {
    TransactionHandler.create(transaction).then(({ status, data }) => {
      if (status == 201) {
        // 요청이 성공적으로 처리되었을 경우
        alert("추가 성공!");
      } else if (status == 400) {
        // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우

        alert(data.message);
      } else if (status == 401) {
        // 	Token이 유효하지 않은 경우
      } else if (status == 403) {
        // 	Token이 없거나 권한이 부족한 경우
      } else if (status == 409) {
        // DB, 메일 전송 오류 등 예상치 못한 오류가 발생한 경우
      } else if (status == 422) {
        // 	요청 파라미터가 유효하지 않은 경우
      }
    });
  };

  const update_transaction = (id, transaction) => {
    TransactionHandler.update(id, transaction).then(({ status, data }) => {
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        alert("수정 성공!");
      }
    });
  };
</script>

<Dialog
  bind:open
  surface$style="width: 550px; max-width: calc(100vw - 32px);"
  aria-labelledby="fullscreen-title"
  aria-describedby="fullscreen-content"
>
  <Header>
    <Title id="fullscreen-title">업무현황 추가</Title>
  </Header>
  <Content id="fullscreen-content">
    {#if Object.keys(tmp_transaction).length !== 0}
      <div class="input-wrap">
        <h3>업무유형</h3>
        <Select
          variant="outlined"
          bind:value={tmp_transaction["insurance_company_id"]}
          style="width:100%;"
          anchor$style="height:36px;"
          selectedText$style="font-size:15px;"
        >
          {#each insurance_company_list as insurance_company}
            <Option value={insurance_company.id}
              >{insurance_company.name}</Option
            >
          {/each}
        </Select>
      </div>
      <div class="input-wrap">
        <div style="display:flex; align-items:center;">
          <Textfield
            variant="outlined"
            bind:value={tmp_transaction["date"]}
            label="날짜"
            type="date"
            style="width:85%; height:36px;"
          />
          <Datepicker
            format={"YYYY-MM-DD"}
            theme={calendar_theme}
            bind:store={date_store}
            let:key
            let:send
            let:receive
            value={{ locale }}
          >
            <div
              variant="unelevated"
              in:receive|local={{ key }}
              out:send|local={{ key }}
            >
              <IconButton class="material-icons">event</IconButton>
            </div>
          </Datepicker>
        </div>
      </div>
      <div class="input-wrap">
        <h3>직원</h3>
        <div>
          <Select
            variant="outlined"
            bind:value={tmp_transaction["user_id"]}
            style="width:100%;"
            anchor$style="height:36px; width:100%;"
          >
            {#each employee_list as employee}
              <Option value={employee.id}>{employee.name}</Option>
            {/each}
          </Select>
        </div>
      </div>
      <div class="input-wrap">
        <h3>차량번호</h3>
        <Textfield
          variant="outlined"
          bind:value={tmp_transaction["vehicle_id"]}
          style="height:36px; width:100%;"
        />
      </div>
      <div class="input-wrap">
        <h3>차종</h3>
        <Textfield
          variant="outlined"
          bind:value={tmp_transaction["vehicle_model"]}
          style="height:36px; width:100%;"
        />
      </div>
      <div class="input-wrap">
        <h3>가격</h3>
        <Textfield
          variant="outlined"
          bind:value={tmp_transaction["price"]}
          style="height:36px; width:100%;"
          suffix="㎏"
          input$pattern="\d+"
        />
      </div>
      <div class="input-wrap">
        <h3>비고</h3>
        <Textfield
          variant="outlined"
          bind:value={tmp_transaction["memo"]}
          style="height:36px; width:100%;"
        />
      </div>
    {/if}
  </Content>
  <Actions>
    <Button
      on:click={() => {
        if (new_transaction) create_transaction(tmp_transaction);
        else update_transaction(tmp_transaction["id"], tmp_transaction);
      }}
    >
      <Label>확인</Label>
    </Button>
  </Actions>
</Dialog>

<style lang="scss">
  .input-wrap {
    margin-bottom: 30px;
  }

  :global(.contents-wrapper) {
    position: fixed !important;
  }
</style>
