library(rvest)
library(magrittr)
library(stringr)

archive = read.csv("archive.csv", stringsAsFactors = F)

# 先按照时间排序
archive$提交时间 = strptime(archive$提交时间, format = "%a %b %d %H:%M:%S %Y")
archive = archive[seq(dim(archive)[1],1),]

# 取提交时间不为空
archive = archive[!is.na(archive$提交时间), ]

# 取最新的N条
N = ifelse(nrow(archive) >= 80, 80, nrow(archive))
archive = archive[1:N, ]

# 提取原始网址并去重
url_pattern <- "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
archive$url = str_extract(archive$原始链接, url_pattern)
archive = archive[!duplicated(archive$url), ]

# check
Get_title = function(url){
  tryCatch({
    node = ifelse(startsWith(url, "https://mp.weixin.qq.com/s"), ".rich_media_title", "title")
    read_html(url) %>%
      html_nodes(node) %>%
      html_text() %>%
      trimws()
  }, error = function(e) {
    print('check failure')
  })
}

archive$check = sapply(archive$url, Get_title)
archive$check = as.character(archive$check)

write.csv(archive[,c(1:4,11,5:10)], "archive2.csv", row.names = F)

rm(list=ls())
gc()
