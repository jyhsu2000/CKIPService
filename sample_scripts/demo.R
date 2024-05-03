library(httr)

url <- "http://localhost:5005"
text <- "土地公有政策?？還是土地婆有政策。.\n最多容納59,000個人,或5.9萬人,再多就不行了.這是環評的結論."

result <- POST(url = url, body = list(
  sentence_list = text
))
content(result, type = 'text', encoding = 'UTF-8')
