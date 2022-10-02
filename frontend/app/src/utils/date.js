export const dateFormatting = (n) => {
  return n >= 10 ? n : "0" + n;
};

export const getToday = (format = "object") => {
  let today = new Date();
  if (format == "object") {
    return {
      year: today.getFullYear(),
      month: today.getMonth() + 1,
      date: today.getDate(),
    };
  } else if (format == "YYYY-MM-DD") {
    return `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;
  }
};

export const isToday = (year, month, date) => {
  let today = getToday();
  if (date == undefined) {
    if (year == today.year && month == today.month) return true;
    else return false;
  } else {
    if (year == today.year && month == today.month && date == today.date)
      return true;
    else return false;
  }
};

export const getSelectableYears = () => {
  let { year } = getToday();
  let selectable_years = [];
  for (let i = 0; i <= 3; i++) selectable_years.push(year - i);
  return selectable_years;
};

export const getTodayString = () => {
  let { year, month, date } = getToday();
  return `${year}-${dateFormatting(month)}-${dateFormatting(date)}`;
};

export const getSelectableMonths = () => {
  let { month } = getToday();
  let selectable_months = [];
  for (let i = 1; i <= month + 1; i++) selectable_months.push(i);
  return selectable_months;
};

export const getSelectableDates = (year, month, day) => {
  let selectable_dates = [];
  let today_month = getToday()["month"];
  if (year == "" || month == "") return selectable_dates;
  if (today_month == month) {
    for (let i = 1; i <= getToday()["date"]; i++) selectable_dates.push(i);
  } else {
    for (let i = 1; i <= 30; i++) selectable_dates.push(i);
  }
  return selectable_dates;
};
