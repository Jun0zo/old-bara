<script>
  import Dialog, { Title, Content, Actions, Header } from "@smui/dialog";
  import Select, { Option } from "@smui/select";
  import Button, { Label } from "@smui/button";
  import Chip, { Set, Text } from "@smui/chips";
  import Textfield from "@smui/textfield";
  import { EmployeeHandler, employee_store } from "~/data/Employee";

  export let open;
  export let target_info;

  let employee_list = [];
  EmployeeHandler.init();
  employee_store.subscribe((value) => {
    if (value.result) employee_list = value.result;
  });

  EmployeeHandler.init();

  let new_user_name = "";
  let new_user_info = {
    name: "",
    role_id: 0,
    status: "accepted",
    plate_fee: 0,
    contract_fee: 0,
    permission_user: "SR",
    permission_transaction: "SR",
    permission_compensation: "SR",
  };

  let permission_choices = ["SR", "AR", "ARW"];
  let role_list = [];

  $: if (open == true) {
    // update name when moal open
    new_user_name = target_info["name"];
  }

  const accept = (user_id, new_user_info) => {
    if (new_user_info["permission_transaction"] == "SR")
      new_user_info["permission_transaction"] = "SRW";
    EmployeeHandler.accept(user_id, new_user_info).then(({ status, data }) => {
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
    });
  };
</script>

<Dialog
  bind:open
  surface$style="width: 550px; max-width: calc(100vw - 32px);"
  aria-labelledby="simple-title2"
  aria-describedby="simple-content2"
>
  <Header id="simple-title2">
    <Title>설정</Title>
  </Header>
  <Content id="simple-content2">
    <div class="role-edit">
      <!-- 기존 정보 변경 -->
      <div class="input-wrap">
        <h3>이름</h3>
        <Textfield
          variant="outlined"
          bind:value={new_user_name}
          style="height:36px; width:100%;"
        />
      </div>
      <div class="input-wrap">
        <h3>직급</h3>
        <div>
          <Select
            variant="outlined"
            bind:value={new_user_info["role_id"]}
            style="width:100%;"
            anchor$style="height:36px; width:100%;"
          >
            {#each role_list as role (role.id)}
              <Option value={role.id}>{role.name}</Option>
            {/each}
          </Select>
        </div>
      </div>
      <div class="input-wrap">
        <h3>지임료</h3>
        <Textfield
          variant="outlined"
          bind:value={new_user_info["plate_fee"]}
          style="height:36px; width:100%;"
        />
      </div>
      <div class="input-wrap">
        <h3>수수료</h3>
        <Textfield
          variant="outlined"
          bind:value={new_user_info["contract_fee"]}
          style="height:36px; width:100%;"
        />
      </div>
      <div class="input-wrap">
        <h3>직원 관리 권한</h3>
        <Set
          chips={permission_choices}
          let:chip
          choice
          bind:selected={new_user_info["permission_user"]}
        >
          <Chip {chip}>
            <Text>
              {#if chip == "SR"}
                {"기본"}
              {:else if chip == "AR"}
                {"중간관리자"}
              {:else if chip == "ARW"}
                {"최고관리자"}
              {/if}
            </Text>
          </Chip>
        </Set>
      </div>
      <div class="input-wrap">
        <h3>업무 관리 권한</h3>
        <Set
          chips={permission_choices}
          let:chip
          choice
          bind:selected={new_user_info["permission_transaction"]}
        >
          <Chip {chip}>
            <Text>
              {#if chip == "SR"}
                {"기본"}
              {:else if chip == "AR"}
                {"중간관리자"}
              {:else if chip == "ARW"}
                {"최고관리자"}
              {/if}
            </Text>
          </Chip>
        </Set>
      </div>
      <div class="input-wrap">
        <h3>추가급여 관리 권한</h3>
        <Set
          chips={permission_choices}
          let:chip
          choice
          bind:selected={new_user_info["permission_compensation"]}
        >
          <Chip {chip}>
            <Text>
              {#if chip == "SR"}
                {"기본"}
              {:else if chip == "AR"}
                {"중간관리자"}
              {:else if chip == "ARW"}
                {"최고관리자"}
              {/if}
            </Text>
          </Chip>
        </Set>
      </div>
    </div>
  </Content>
  <Actions>
    <Button>
      <Label>No</Label>
    </Button>
    <Button
      on:click={() => {
        accept(target_info["id"]);
      }}
    >
      <Label>Yes</Label>
    </Button>
  </Actions>
</Dialog>

<style>
  .input-wrap {
    margin-bottom: 30px;
  }
</style>
