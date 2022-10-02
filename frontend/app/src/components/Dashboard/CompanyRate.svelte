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
    "/api/dashboard/current-month-invoice-company-rate",
    "get",
    {},
    {},
    "access"
  ).then(({ status, data }) => {
    if (status == 200) {
      // 요청이 성공적으로 처리되었을 경우
      names = data.result.company_list.map((info) => info.company_name);
      percentages = data.result.company_list.map((info) => info.percentage);
      diff_percentages = data.result.company_list.map(
        (info) => info.difference_percentage
      );
      companys = data.result.company_list.map((info) => ({
        name: info.company_name,
        diff_percentages: info.difference_percentage,
      }));
    }
  });
  let options = {};
  let companys = [];
  $: options = {
    series: percentages,
    labels: names,
    chart: {
      type: "donut",
      toolbar: {
        show: false,
      },
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
  <Head>업무 유형</Head>
  <Body>
    <div class="chart-wrap" use:chart={options} />
    <div class="type-list">
      {#each companys as company}
        <div class="type">
          {#if company.diff_percentages > 0}
            <FontAwesomeIcon icon={faArrowTrendUp} style="color:green" />
          {:else}
            <FontAwesomeIcon icon={faArrowTrendDown} style="color:red" />
          {/if}
          <div class="diff-percentages">
            {company.diff_percentages}%
          </div>
          <div class="name">{company.name}</div>
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
