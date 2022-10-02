<script>
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import Button, { Label } from "@smui/button";

  import Template from "~/templates/Template.svelte";
  import BaraCard, { Head, Body } from "~/components/bara-card";

  import RoleModal from "~/components/Employee/RoleModal.svelte";
  import AcceptedTable from "~/components/Employee/AcceptedTable.svelte";
  import VerifiedTable from "~/components/Employee/VerifiedTable.svelte";
  import DeletedTable from "~/components/Employee/DeletedTable.svelte";

  let nav_info = { active_name: "employee", title_name: "Employee List" };
  let role_modal_open = false;
</script>

<Template {nav_info}>
  <div class="action-wrap">
    <Button
      variant="unelevated"
      style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
      on:click={() => {
        console.log(role_modal_open);
        role_modal_open = true;
      }}
    >
      <Label>직급수정</Label>
    </Button>
  </div>

  <LayoutGrid class="p-0">
    <Cell spanDevices={{ desktop: 12, tablet: 12, phone: 12 }}>
      <BaraCard>
        <Head>직원</Head>
        <Body>
          <AcceptedTable />
        </Body>
      </BaraCard>
    </Cell>

    <Cell spanDevices={{ desktop: 6, tablet: 12, phone: 12 }}>
      <BaraCard>
        <Head>승인대기</Head>
        <Body>
          <VerifiedTable />
        </Body>
      </BaraCard>
    </Cell>
    <Cell spanDevices={{ desktop: 6, tablet: 12, phone: 12 }}>
      <BaraCard>
        <Head>탈퇴처리</Head>
        <Body>
          <DeletedTable />
        </Body>
      </BaraCard>
    </Cell>
  </LayoutGrid>
</Template>

<RoleModal bind:open={role_modal_open} />

<style lang="scss">
  :global(.content) {
    width: 100%;
  }

  .action-wrap {
    display: flex;
    justify-content: flex-end;
    padding: 30px 0px;
  }
</style>
