<script>
  import { chart } from "svelte-apexcharts";

  import {
    faArrowTrendUp,
    faArrowTrendDown,
  } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "fontawesome-svelte";

  import BaraCard, { Head, Body } from "~/components/bara-card";
  import { request } from "~/utils/request";

  let names = [];
  let percentages = [];
  let diff_percentages = [];

  request(
    "/api/dashboard/current-month-member-revenue-rate",
    "get",
    {},
    {},
    "access"
  ).then(({ status, data }) => {
    if (status == 200) {
      // 요청이 성공적으로 처리되었을 경우
      names = data.result.user_list.map((info) => info.user_name);
      percentages = data.result.user_list.map((info) => info.percentage);
      diff_percentages = data.result.user_list.map(
        (info) => info.difference_percentage
      );
      transaction_types = data.result.user_list.map((info) => ({
        user_name: info.user_name,
        diff_percentages: info.difference_percentage,
      }));

      
    }
  });

  let options = {};
  let transaction_types = [];
  $: options = {
    series: percentages,
    labels: names,
    chart: {
      type: "donut",
      toolbar: {
        show: false,
      },
      animations: {
        enabled:true
      }
    },

    legend: {
      // 옆에 설명
      show: false,
    },
    dataLabels: {
      enabled: false,
    },
    plotOptions: {
      pie: {
        expandOnClick: false,
      },
    },
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: {
            width: 200,
          },
          legend: {
            position: "bottom",
          },
        },
      },
    ],
  };
</script>

<BaraCard>
  <Head>직원 매출 비율</Head>
  <Body>
    <div class="chart-wrap" use:chart={options} />
    <div class="type-list">
      {#each transaction_types as transaction_type}
        <div class="type">
          {#if transaction_type.diff_percentages > 0}
            <FontAwesomeIcon icon={faArrowTrendUp} style="color:green" />
          {:else}
            <FontAwesomeIcon icon={faArrowTrendDown} style="color:red" />
          {/if}
          <div class="diff-percentages">
            {transaction_type.diff_percentages}%
          </div>
          <div class="name">{transaction_type.user_name}</div>
        </div>
      {/each}
    </div>
  </Body>
</BaraCard>

<style>
  .chart-wrap {
    display: flex;
    justify-content: center;
  }

  .type-list {
    display: flex;
    justify-content: space-around;
  }

  .type {
    text-align: center;
    margin-top: 15px;
  }

  .type .name {
    font-size: 14px;
    color: var(--bara-text-mutted);
  }

  .type .diff-percentages {
    font-size: 24px;
    padding: 10px 0px;
  }
</style>
