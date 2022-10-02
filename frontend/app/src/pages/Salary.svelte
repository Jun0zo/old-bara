<script>
  import Template from "~/templates/Template.svelte";
  import BaraCard, { Head, Body } from "~/components/bara-card";
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import Select, { Option } from "@smui/select";

  import UserInvoice from "~/components/Salary/UserInvoice.svelte";
  import CompanyInvoice from "~/components/Salary/CompanyInvoice.svelte";

  import {
    getToday,
    getSelectableYears,
    getSelectableMonths,
  } from "~/utils/date";

  let nav_info = { active_name: "salary", title_name: "Salary" };

  let today = getToday();
  let year = today["year"];
  let month = today["month"];
</script>

<Template {nav_info}>
  <div class="head-wrap">
    <Select
      style="width:100px; margin-right:15px;"
      anchor$style="height:40px;"
      variant="outlined"
      bind:value={year}
      label="년"
    >
      {#each getSelectableYears() as year}
        <Option value={String(year)}>{year}</Option>
      {/each}
    </Select>

    <Select
      style="width:100px;"
      anchor$style="height:40px;"
      variant="outlined"
      bind:value={month}
      label="월"
    >
      {#each getSelectableMonths() as month}
        <Option value={String(month)}>{month}</Option>
      {/each}
    </Select>
  </div>

  <LayoutGrid style="padding-left:0px; padding-right:0px;">
    <Cell spanDevices={{ desktop: 6, tablet: 6, phone: 12 }}>
      <BaraCard>
        <Head>직원급여현황</Head>
        <Body>
          <UserInvoice {year} {month} />
        </Body>
      </BaraCard>
    </Cell>
    <Cell spanDevices={{ desktop: 6, tablet: 6, phone: 12 }}>
      <BaraCard>
        <Head>회사급여현황</Head>
        <Body>
          <CompanyInvoice {year} {month} />
        </Body>
      </BaraCard>
    </Cell>
  </LayoutGrid>
</Template>

<style lang="scss">
  .head-wrap {
    display: flex;
    justify-content: flex-end;
  }
</style>
