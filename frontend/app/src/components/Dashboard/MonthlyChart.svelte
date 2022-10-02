<script>
  import { chart } from "svelte-apexcharts";
  import { request } from "~/utils/request";

  // request("/api/dashboard/staff/daily/profit", "get", {}, {}, "access").then(
  //   ({ status, data }) => {
  //     // console.log(status, data);
  //     // console.log(data)
  //   }
  // );

  let revenues = [];
  let dates = [];

  request("/api/dashboard/monthly-revenue/6", "get", {}, {}, "access").then(
    ({ status, data }) => {
      if (status == 200) {
        // 요청이 성공적으로 처리되었을 경우
        revenues = data.result.revenue_list.map((info) => info.revenue);
        dates = data.result.revenue_list.map(
          (info) => `${info.year}/${info.month}`
        );
      } else if (status == 400) {
        // 요청 파라미터의 Type은 유효하나 함수 내부에서 Validation이 실패할 경우
      } else if (status == 401) {
        // 	Token이 유효하지 않은 경우
      } else if (status == 403) {
        // 	Token이 없거나 권한이 부족한 경우
      }
    }
  );

  let options = {};
  $: options = {
    colors: ["#727cf5", "#e3eaee"],
    chart: {
      type: "bar",
      foreColor: "#adb5bd",
      stacked: true,
      toolbar: {
        show: false,
      },
    },
    plotOptions: {
      bar: {
        columnWidth: "45%",
      },
    },

    dataLabels: {
      // bar 내부 글씨
      enabled: false,
    },
    legend: {
      // 옆에 설명
      show: false,
    },
    series: [
      {
        name: "수수료",
        data: revenues,
      },
      {
        name: "취소수수료",
        data: [2, 10, 5, 12, 20, 1],
      },
    ],
    xaxis: {
      categories: dates,
    },
    grid: {
      xaxis: {
        show: false,
      },
    },
  };
</script>

<div use:chart={options} />
