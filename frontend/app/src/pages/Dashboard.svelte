<script>
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import Template from "~/templates/Template.svelte";

  import {
    MemberRevenue,
    MonthlyChart,
    Overall,
    MemberRevenueRate,
    CompanyRate,
  } from "~/components/Dashboard";

  import BaraCard, { Head, Body } from "~/components/bara-card";
  let nav_info = { active_name: "dashboard", title_name: "Dashboard" };
</script>

<Template {nav_info}>
  <LayoutGrid class="p-0">
    <Cell
      style="height:100%;"
      
      spanDevices={{ desktop: 6, tablet: 12, phone: 12 }}
    >
      <Overall />
    </Cell>
    <Cell spanDevices={{ desktop: 6, tablet: 12, phone: 12 }}>
      <BaraCard>
        <Head>월별 수수료</Head>
        <Body>
          <MonthlyChart />
        </Body>
      </BaraCard>
    </Cell>
    <Cell spanDevices={{ desktop: 4, tablet: 12, phone: 12 }}>
      <MemberRevenue />
    </Cell>
    <Cell spanDevices={{ desktop: 4, tablet: 12, phone: 12 }}>
      <MemberRevenueRate />
    </Cell>
    <Cell spanDevices={{ desktop: 4, tablet: 12, phone: 12 }}>
      <CompanyRate />
    </Cell>
  </LayoutGrid>
</Template>

<style>
</style>
