/* Shared formatter for dated, source-backed opening hours.
 * Never claim "open now": these are published ordinary weekly patterns,
 * not confirmed special-date service, and may be out of date.
 */
(() => {
  "use strict";
  const DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
  const LABELS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  function displayClock(clock) {
    const [hours, minutes] = clock.split(":").map(Number);
    return hours >= 24
      ? String(hours - 24).padStart(2, "0") + ":" +
        String(minutes).padStart(2, "0") + " (+1 day)"
      : clock;
  }

  function displayPeriods(intervals) {
    if (!Array.isArray(intervals)) return "Not verified";
    if (!intervals.length) return "Closed (published schedule)";
    return intervals.map(([start, end]) =>
      displayClock(start) + "–" + displayClock(end)).join(", ");
  }

  function dayKey(isoDate) {
    // Parse the local calendar date as an ISO calendar day, not a UTC timestamp.
    const date = new Date(isoDate + "T12:00:00Z");
    if (Number.isNaN(date.valueOf())) return null;
    return DAYS[(date.getUTCDay() + 6) % 7];
  }

  function displayHours(entry, day, food = false) {
    if (!entry) return "Hours not verified";
    if (entry.status === "event-only") return "Event-only — check producer";
    const timetable = food ? entry.food_days : entry.days;
    if (!timetable) return food ? "Kitchen times not verified" : "Hours not verified";
    return displayPeriods(timetable[day]);
  }

  function isPublishedOpen(entry, day) {
    return Boolean(entry && entry.status === "published" &&
      Array.isArray(entry.days?.[day]) && entry.days[day].length);
  }

  function sourceName(entry) {
    return entry?.source_type === "official" ? "Operator" : "CAMRA / local branch";
  }

  window.BeerTripHours = Object.freeze({
    DAYS, LABELS, dayKey, displayClock, displayPeriods, displayHours,
    isPublishedOpen, sourceName,
  });
})();
