<script>
  import { chart } from "svelte-apexcharts";
  import BaraCard, { Head, Body } from "~/components/bara-card";

  import { request } from "~/utils/request";

  let user_infos = [];
  request(
    "/api/dashboard/monthly-member-revenue",
    "get",
    {},
    {},
    "access"
  ).then(({ status, data }) => {
    if (status == 200) {
      // 요청이 성공적으로 처리되었을 경우
      user_infos = data.result.user_list.map((info) => ({
        x: info.user_name,
        y: info.revenue,
      }));
    }
  });

  let options = {};
  $: options = {
    chart: {
      type: "bar",
      toolbar: {
        show: false,
      },
    },
    plotOptions: {
      bar: {
        horizontal: true,
      },
    },
    dataLabels: {
      // bar 내부 글씨
      enabled: false,
    },
    series: [
      {
        data: user_infos,
      },
    ],
  };
</script>

<BaraCard>
  <Head>직원 별 매출</Head>
  <Body>
    <div use:chart={options} />
  </Body>
</BaraCard>

<style>
</style>
