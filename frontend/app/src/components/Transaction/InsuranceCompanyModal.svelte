<script>
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import Dialog, { Title, Content, Actions, Header } from "@smui/dialog";
  import Textfield from "@smui/textfield";

  import { faPlusCircle } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "fontawesome-svelte";
  import Button, { Label } from "@smui/button";

  import List, {
    Item,
    Graphic,
    Meta,
    Text,
    PrimaryText,
    SecondaryText,
  } from "@smui/list";

  import {
    InsuranceCompanyHandler,
    insurance_company_store,
  } from "~/data/InsuranceCompany";

  export let open;

  let new_name = "";

  let insurance_company_list = [];
  InsuranceCompanyHandler.init();
  insurance_company_store.subscribe((value) => {
    console.log("test console ", value.result);
    if (value.result) insurance_company_list = value.result;
  });

  let selection_id = 0;
  $: selection_info = insurance_company_list.filter(
    (insurance_company) => insurance_company.id == selection_id
  )[0];
  let selectionIndex;

  $: if (open == true) {
    // update name when moal open
    new_name = "";
  }

  const create_company = (name) => {
    InsuranceCompanyHandler.create(name).then(({ status, data }) => {
      if (status == 201) {
        // 요청이 성공적으로 처리되었을 경우
        alert("추가 성공!");
      } else if (status == 400) {
        // 	요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
        // 1. 사명은 2자 이상, 10자 이하여야 합니다!"
        alert(data.message);
      } else if (status == 401) {
        // 	Token이 유효하지 않은 경우
        // 1. 이미 존재하는 회사입니다!
        alert(data.message);
      } else if (status == 403) {
        // 	Token이 없거나 권한이 부족한 경우
      } else if (status == 409) {
        // DB, 메일 전송 오류 등 예상치 못한 오류가 발생한 경우
      } else if (status == 422) {
        // 	요청 파라미터가 유효하지 않은 경우
      }
    });
  };

  const delete_company = (id) => {
    InsuranceCompanyHandler.delete(id).then(({ status, data }) => {
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        alert("삭제 성공!");
      } else if (status == 400) {
        // 	요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
        // 1. 해당 보험사와 발생한 거래가 1건 이상 존재합니다!↵데이터 무결성을 위해 거래가 존재하는 보험사는 삭제할 수 없습니다!
        alert(data.message);
      }
    });
  };

  const update_company = (id, name) => {
    console.log(id, name);
    InsuranceCompanyHandler.update(id, name).then(({ status, data }) => {
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        alert("추가 성공!");
      }
    });
  };
</script>

<Dialog
  bind:open
  fullscreen
  aria-labelledby="fullscreen-title"
  aria-describedby="fullscreen-content"
>
  <!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
  <Header>
    <Title id="fullscreen-title">Terms and Conditions</Title>
  </Header>
  <Content id="fullscreen-content">
    <LayoutGrid>
      <Cell spanDevices={{ desktop: 6, tablet: 6, phone: 12 }}>
        <div class="company-list">
          <List
            class="demo-list"
            twoLine
            avatarList
            singleSelection
            bind:selectedIndex={selectionIndex}
          >
            {#each insurance_company_list as insurance_company}
              <Item
                on:SMUI:action={() => (selection_id = insurance_company.id)}
                selected={selection_id === insurance_company.id}
              >
                <Graphic
                  style="background-image: url(https://place-hold.it/40x40?text={insurance_company.name
                    .split(' ')
                    .map((val) => val.substring(0, 1))
                    .join('')}&fontsize=16);
                      "
                />
                <Text>
                  <PrimaryText>{insurance_company.name}</PrimaryText>
                  <SecondaryText>{insurance_company.id}</SecondaryText>
                </Text>
                <Meta class="material-icons">info</Meta>
              </Item>
            {/each}
            <Item
              on:SMUI:action={() => (selection_id = 0)}
              selected={selection_id === 0}
            >
              <Graphic
                ><FontAwesomeIcon
                  style="width:40px; height:40px; color:#aaaaaa;"
                  icon={faPlusCircle}
                /></Graphic
              >

              <Text>
                <PrimaryText>추가하기</PrimaryText>
                <SecondaryText />
              </Text>
            </Item>
          </List>
        </div>
      </Cell>
      <Cell spanDevices={{ desktop: 6, tablet: 6, phone: 12 }}>
        <div class="company-edit">
          {#if selection_info}
            <!-- 기존 정보 변경 -->
            <div class="input-wrap">
              <h3>회사명</h3>
              <Textfield
                variant="outlined"
                bind:value={selection_info["name"]}
                style="height:36px; width:100%;"
              />
            </div>
            <div class="action-wrap">
              <Button
                variant="unelevated"
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                on:click={() => delete_company(selection_id)}
              >
                <Label>삭제</Label>
              </Button>
              <Button
                variant="unelevated"
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                on:click={() =>
                  update_company(selection_id, selection_info["name"])}
              >
                <Label>적용</Label>
              </Button>
            </div>
          {:else if selection_id == 0}
            <!-- 새로 추가  -->
            <div class="input-wrap">
              <h3>회사명</h3>
              <Textfield
                variant="outlined"
                bind:value={new_name}
                style="height:36px; width:100%;"
              />
            </div>
            <div class="action-wrap">
              <Button
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                variant="unelevated"
                on:click={() => create_company(new_name)}
              >
                <Label>추가</Label>
              </Button>
            </div>
          {/if}
        </div>
      </Cell>
    </LayoutGrid>
  </Content>
  <Actions>
    <Button>
      <Label>확인</Label>
    </Button>
  </Actions>
</Dialog>

<style lang="scss">
  .company-list {
    height: 250px;
    border: 1px solid #9e9e9e;
    border-radius: 10px;
    padding: 10px 0px;
    overflow-y: scroll;
  }

  .company-edit {
    height: 250px;
    border: 1px solid #9e9e9e;
    border-radius: 10px;
    padding: 10px 50px;
    .input-wrap {
      margin-bottom: 30px;
    }
  }

  .action-wrap {
    display: flex;
    justify-content: flex-end;
    padding: 30px 0px;
  }
</style>
