library(rvest)
library(magrittr)

archive = read.csv("archive.csv", header = F, stringsAsFactors = F)

Get_title = function(url){
  read_html(url) %>%
    html_nodes("title") %>%
    html_text()
}

archive$title = sapply(archive$V2, Get_title)
write.csv(archive, "archive2.csv", row.names = F)
