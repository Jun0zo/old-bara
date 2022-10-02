<script>
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import Select, { Option } from "@smui/select";
  import Textfield from "@smui/textfield";
  import IconButton from "@smui/icon-button";

  import { EmployeeHandler, employee_store } from "~/data/Employee";
  import {
    InsuranceCompanyHandler,
    insurance_company_store,
  } from "~/data/InsuranceCompany";
  import { calendar_theme, locale } from "~/data/date_picker_settings";
  import { Datepicker } from "svelte-calendar";
  import dayjs from "dayjs";

  export let option;

  let canceled_type_list = ["ALL", "EXCLUDE_CANCELED", "CANCELED_ONLY"];

  let employee_list = [];
  EmployeeHandler.init();
  employee_store.subscribe((value) => {
    if (value.result) employee_list = value.result;
  });

  let insurance_company_list = [];
  InsuranceCompanyHandler.init();
  insurance_company_store.subscribe((value) => {
    if (value.result) insurance_company_list = value.result;
  });

  let start_date_store;
  let end_date_store;

  option["start_date"] = dayjs().format("YYYY-MM-DD");
  option["end_date"] = dayjs().format("YYYY-MM-DD");

  $: {
    if ($start_date_store?.hasChosen) {
      option["start_date"] = dayjs($start_date_store.selected).format(
        "YYYY-MM-DD"
      );
    }

    if ($end_date_store?.hasChosen) {
      option["end_date"] = dayjs($end_date_store.selected).format("YYYY-MM-DD");
    }
  }

  setInterval(() => {
    console.log(option);
  }, 5000);
</script>

<LayoutGrid>
  <Cell spanDevices={{ desktop: 6, tablet: 12, phone: 12 }}>
    <Select
      style="width:100px;"
      anchor$style="height:40px;"
      variant="outlined"
      bind:value={option["user_id"]}
      label="직원"
    >
      <Option value="">전체</Option>
      {#each employee_list as employee}
        <Option value={String(employee.id)}>{employee.name}</Option>
      {/each}
    </Select>

    <Select
      variant="outlined"
      style="width:140px;"
      anchor$style="height:40px;"
      bind:value={option["canceled_type"]}
      label="취소건"
    >
      {#each canceled_type_list as canceled_type}
        <Option value={canceled_type}>
          {#if canceled_type == "ALL"}
            {"전체"}
          {:else if canceled_type == "EXCLUDE_CANCELED"}
            {"취소건 제외"}
          {:else if canceled_type == "CANCELED_ONLY"}
            {"취소건"}
          {/if}
        </Option>
      {/each}
    </Select>

    <Select
      variant="outlined"
      style="width:140px;"
      anchor$style="height:40px;"
      bind:value={option["insurance_company_id"]}
      label="제휴사"
    >
      <Option value="-1">전체</Option>
      {#each insurance_company_list as insurance_company}
        <Option value={String(insurance_company.id)}>
          {insurance_company.name}
        </Option>
      {/each}
    </Select>
  </Cell>

  <Cell spanDevices={{ desktop: 6, tablet: 12, phone: 12 }}>
    <LayoutGrid class="p-0">
      <Cell spanDevices={{ desktop: 6, tablet: 12, phone: 12 }}>
        <div style="display:flex; align-items:center;">
          <Textfield
            variant="outlined"
            bind:value={option["start_date"]}
            label="시작날짜"
            type="date"
            style="width:80%; height:40px;"
          />
          <Datepicker
            format={"YYYY-MM-DD"}
            theme={calendar_theme}
            bind:store={start_date_store}
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
      </Cell>
      <Cell spanDevices={{ desktop: 6, tablet: 12, phone: 12 }}>
        <div style="display:flex; align-items:center;">
          <Textfield
            variant="outlined"
            bind:value={option["end_date"]}
            label="끝날짜"
            type="date"
            style="width:80%; height:40px;"
          />
          <Datepicker
            format={"YYYY-MM-DD"}
            theme={calendar_theme}
            bind:store={end_date_store}
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
      </Cell>
    </LayoutGrid>
  </Cell>
  <Cell>
    <Select
      variant="outlined"
      style="width:140px;"
      anchor$style="height:40px;"
      bind:value={option["order_by"]}
      label="정렬기준"
    >
      <Option value="transaction_id">거래순</Option>
      <Option value="price">금액</Option>
      <Option value="cancel_fee">취소수수료</Option>
    </Select>

    <Select
      variant="outlined"
      style="width:140px;"
      anchor$style="height:40px;"
      bind:value={option["order_type"]}
      label="정렬순서"
    >
      <Option value="desc">내림차순</Option>
      <Option value="asc">오름차순</Option>
    </Select>
  </Cell>
</LayoutGrid>
