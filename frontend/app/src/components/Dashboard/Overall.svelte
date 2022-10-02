<script>
  import LayoutGrid, { Cell } from "@smui/layout-grid";

  import BaraCard, { Head, Body } from "~/components/bara-card";

  import {
    faLongArrowAltUp,
    faLongArrowAltDown,
    faUsers,
  } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "fontawesome-svelte";

  import { request } from "~/utils/request";

  let overall_data = {
    current_month_revenue: { revenue: 0, difference_count: 0 },
    current_day_revenue: { revenue: 0, difference_count: 0 },
    current_month_transaction_count: {
      transaction_count: 0,
      difference_count: 0,
    },
    current_day_transaction_count: {
      transaction_count: 0,
      difference_count: 0,
    },
  };

  request("/api/dashboard/current-month-revenue", "get", {}, {}, "access").then(
    ({ status, data }) => {
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        overall_data.current_month_revenue = data.result;
      } else if (status == 400) {
        // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
      } else if (status == 401) {
        // 	Token이 유효하지 않은 경우
      } else if (status == 403) {
        // 	Token이 없거나 권한이 부족한 경우
      }
    }
  );

  request("/api/dashboard/current-day-revenue", "get", {}, {}, "access").then(
    ({ status, data }) => {
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        overall_data.current_day_revenue = data.result;
      } else if (status == 400) {
        // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
      } else if (status == 401) {
        // 	Token이 유효하지 않은 경우
      } else if (status == 403) {
        // 	Token이 없거나 권한이 부족한 경우
      }
    }
  );

  request(
    "/api/dashboard/current-month-transaction-count",
    "get",
    {},
    {},
    "access"
  ).then(({ status, data }) => {
    if (status == 200) {
      // 요청이 성공적으로 처리되었을 경우
      overall_data.current_month_transaction_count = data.result;
    } else if (status == 400) {
      // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
    } else if (status == 401) {
      // 	Token이 유효하지 않은 경우
    } else if (status == 403) {
      // 	Token이 없거나 권한이 부족한 경우
    }
  });

  request(
    "/api/dashboard/current-day-transaction-count",
    "get",
    {},
    {},
    "access"
  ).then(({ status, data }) => {
    if (status == 200) {
      // 요청이 성공적으로 처리되었을 경우
      overall_data.current_day_transaction_count = data.result;
    } else if (status == 400) {
      // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
    } else if (status == 401) {
      // 	Token이 유효하지 않은 경우
    } else if (status == 403) {
      // 	Token이 없거나 권한이 부족한 경우
    }
  });
</script>

<LayoutGrid style="padding:0px;">
  <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 12 }}>
    <BaraCard>
      <Body>
        <div class="icon">
          <FontAwesomeIcon icon={faUsers} style="color:#727cf5;" />
        </div>
        <div class="title">매출액</div>
        <div class="now">{overall_data.current_month_revenue.revenue}</div>
        <div class="increase">
          {#if overall_data.current_month_revenue.difference_percentage > 0}
            <strong class="green">
              <FontAwesomeIcon icon={faLongArrowAltUp} />
              {overall_data.current_month_revenue.difference_percentage} %
            </strong>
          {:else if overall_data.current_month_revenue.difference_percentage < 0}
            <strong class="red">
              <FontAwesomeIcon icon={faLongArrowAltDown} />
              {overall_data.current_month_revenue.difference_percentage} %
            </strong>
          {:else}
            <strong class="gray">
              {overall_data.current_month_revenue.difference_percentage} %
            </strong>
          {/if}

          <span>전월 대비</span>
        </div>
      </Body>
    </BaraCard>
  </Cell>
  <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 12 }}>
    <BaraCard>
      <Body>
        <div class="icon">
          <FontAwesomeIcon icon={faUsers} style="color:#727cf5;" />
        </div>
        <div class="title">거래발생개수</div>
        <div class="now">
          {overall_data.current_month_transaction_count.transaction_count}
        </div>
        <div class="increase">
          {#if overall_data.current_month_transaction_count.difference_count > 0}
            <strong class="green">
              <FontAwesomeIcon icon={faLongArrowAltUp} />
              {overall_data.current_month_transaction_count.difference_count} %
            </strong>
          {:else if overall_data.current_month_transaction_count.difference_count < 0}
            <strong class="red">
              {overall_data.current_month_transaction_count.difference_count} %
            </strong>
          {:else}
            <strong class="gray">
              {overall_data.current_month_transaction_count.difference_count} %
            </strong>
          {/if}

          <span>전월 대비</span>
        </div>
      </Body>
    </BaraCard>
  </Cell>
  <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 12 }}>
    <BaraCard>
      <Body>
        <div class="icon">
          <FontAwesomeIcon icon={faUsers} style="color:#727cf5;" />
        </div>
        <div class="title">매출액</div>
        <div class="now">
          {overall_data.current_day_revenue.revenue}
        </div>
        <div class="increase">
          {#if overall_data.current_day_revenue.difference_percentage > 0}
            <strong class="green">
              <FontAwesomeIcon icon={faLongArrowAltUp} />
              {overall_data.current_day_revenue.difference_percentage} %
            </strong>
          {:else if overall_data.current_day_revenue.difference_percentage < 0}
            <strong class="red">
              {overall_data.current_day_revenue.difference_percentage} %
            </strong>
          {:else}
            <strong class="gray">
              {overall_data.current_day_revenue.difference_percentage} %
            </strong>
          {/if}

          <span>전일 대비</span>
        </div>
      </Body>
    </BaraCard>
  </Cell>
  <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 12 }}>
    <BaraCard>
      <Body>
        <div class="icon">
          <FontAwesomeIcon icon={faUsers} style="color:#727cf5;" />
        </div>
        <div class="title">거래발생개수</div>
        <div class="now">12</div>
        <div class="increase">
          {#if overall_data.current_day_transaction_count.difference_count > 0}
            <strong class="green">
              <FontAwesomeIcon icon={faLongArrowAltUp} />
              {overall_data.current_day_transaction_count.difference_count} %
            </strong>
          {:else if overall_data.current_day_transaction_count.difference_count < 0}
            <strong class="red">
              {overall_data.current_day_transaction_count.difference_count} %
            </strong>
          {:else}
            <strong class="gray">
              {overall_data.current_day_transaction_count.difference_count} %
            </strong>
          {/if}
          <span>전일 대비</span>
        </div>
      </Body>
    </BaraCard>
  </Cell>
</LayoutGrid>

<style>
  .title {
    margin-bottom: 15px;
    color: #99a7ad;
  }

  .now {
    margin: 24px 0px;
    color: #6c757d;
    font-size: 23px;
    font-weight: 700;
  }

  .increase {
    display: flex;
    flex-direction: column;
    font-size: 13px;
    line-height: 15px;
    color: #99a7ad;
  }

  .increase strong {
    font-size: 15px;
    font-weight: 600;
    line-height: 20px;
    padding: 5px 0px;
  }

  .green {
    color: #0ccf97;
  }

  .red {
    color: #fa5c7c;
  }

  .gray {
    color: gray;
  }

  .icon {
    border-radius: 3px;
    background-color: rgba(114, 124, 245, 0.25);
    width: 40px;
    height: 40px;
    float: right !important;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
