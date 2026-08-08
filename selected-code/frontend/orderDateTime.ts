const timezoneSuffixPattern = /(Z|[+-]\d{2}:?\d{2})$/i

function parseOrderTimestamp(value: string) {
  return new Date(timezoneSuffixPattern.test(value) ? value : `${value}Z`)
}

export function formatOrderDate(value: string) {
  return new Intl.DateTimeFormat('en-CA', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  }).format(parseOrderTimestamp(value))
}

export function formatOrderDateTime(value: string) {
  return new Intl.DateTimeFormat('en-GB', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(parseOrderTimestamp(value))
}
