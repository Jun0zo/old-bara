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
    CompanyExtraHandler,
    company_extra_store,
  } from "~/data/Invoice/CompanyExtra";

  export let open;
  export let year;
  export let month;

  let company_extra_list = [];

  let selection_info = {};
  $: selection_info = company_extra_list.filter(
    (company_extra) => company_extra.id == selection_id
  )[0];

  company_extra_store.subscribe((value) => {
    if (value.result) company_extra_list = value.result;
  });

  let new_name = "";
  let new_price = 0;
  $: {
    if (year != undefined && month != undefined)
      CompanyExtraHandler._update(year, month);
  }
  let selection_id = 0;
  let selection_index;

  $: if (open == true) {
    // update name when moal open
    new_name = "";
  }

  const createCompanyExtra = (extra_name) => {
    CompanyExtraHandler.create(extra_name).then(({ status, data }) => {
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        alert("추가 성공!");
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

  const deleteCompanyExtra = (extra_id) => {
    CompanyExtraHandler.delete(extra_id).then(({ status, data }) => {
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        alert("삭제 성공!");
      }
    });
  };

  const updateCompanyExtra = (extra_id, extra_name) => {
    console.log(extra_id, extra_name);
    CompanyExtraHandler.update(extra_id, extra_name).then(
      ({ status, data }) => {
        if (status == 200) {
          // 요청이 성공적으로 처리되었을 경우
          alert("추가 성공!");
        }
      }
    );
  };
</script>

<Dialog bind:open fullscreen>
  <Header>
    <Title>{year}년 {month}월 추가급여 현황</Title>
  </Header>
  <Content>
    <LayoutGrid>
      <Cell spanDevices={{ desktop: 6, tablet: 6, phone: 12 }}>
        <div class="extra-list">
          <List
            class="demo-list"
            twoLine
            avatarList
            singleSelection
            bind:selectedIndex={selection_index}
          >
            {#each company_extra_list as extra}
              <Item
                on:SMUI:action={() => (selection_id = extra.id)}
                selected={selection_id === extra.id}
              >
                <Graphic
                  style="background-image: url(https://place-hold.it/40x40?text={extra.name
                    .split(' ')
                    .map((val) => val.substring(0, 1))
                    .join('')}&fontsize=16);
                      "
                />
                <Text>
                  <PrimaryText>{extra.name}</PrimaryText>
                  <SecondaryText>{extra.id}</SecondaryText>
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
        <div class="extra-edit">
          {#if selection_info}
            <!-- 기존 정보 변경 -->
            <div class="input-wrap">
              <h3>보너스명</h3>
              <Textfield
                variant="outlined"
                bind:value={selection_info["name"]}
                style="height:36px; width:100%;"
              />
              <h3>금액</h3>
              <Textfield
                variant="outlined"
                bind:value={selection_info["price"]}
                style="height:36px; width:100%;"
              />
            </div>
            <div class="action-wrap">
              <Button
                variant="unelevated"
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                on:click={() => deleteCompanyExtra(selection_id)}
              >
                <Label>삭제</Label>
              </Button>
              <Button
                variant="unelevated"
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                on:click={() =>
                  deleteCompanyExtra(selection_id, selection_info["name"])}
              >
                <Label>적용</Label>
              </Button>
            </div>
          {:else if selection_id == 0}
            <!-- 새로 추가  -->
            <div class="input-wrap">
              <h3>보너스명</h3>
              <Textfield
                variant="outlined"
                bind:value={new_name}
                style="height:36px; width:100%;"
              />
              <h3>금액</h3>
              <Textfield
                variant="outlined"
                bind:value={new_price}
                style="height:36px; width:100%;"
              />
            </div>
            <div class="action-wrap">
              <Button
                style="background-color:#727cf5; box-shadow:0 2px 6px 0 rgb(114 124 245 / 50%); "
                variant="unelevated"
                on:click={() => createCompanyExtra(new_name)}
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
  .extra-list {
    height: 250px;
    border: 1px solid #9e9e9e;
    border-radius: 10px;
    padding: 10px 0px;
    overflow-y: scroll;
  }

  .extra-edit {
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
