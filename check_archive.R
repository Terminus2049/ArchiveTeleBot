library(rvest)
library(magrittr)
library(readr)

archive = read_csv("archive.csv", col_names = F)

names(archive) = c('Time', 'Title_url', 'Archive_url', 'Title')
archive$Time = substr(archive$Time, 5, nchar(archive$Time))
archive$Time = parse_datetime(archive$Time, format = "%b %d %H:%M:%S %Y")
archive$Time = archive$Time + 8*60*60

archive = archive[!duplicated(archive$Archive_url), ]
archive = archive[!is.na(archive$Title_url), ]

archive = archive[seq(dim(archive)[1],1),]

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

N = ifelse(nrow(archive) >= 60, 60, nrow(archive))
archive = archive[1:N, ]

archive$check = sapply(archive$Title_url, Get_title)
archive$check = as.character(archive$check)

createLink <- function(link, text) {
  paste0('<a href="', link,
         '" target="_blank" class="btn btn-primary">', text, '</a>')
}

archive$Title = ifelse(nchar(archive$Title) > 20, substr(archive$Title, 1, 20), archive$Title)
archive$Title_url = ifelse(startsWith(archive$Title_url, "https://mp.weixin.qq.com/s"),
                            archive$Title,
                            createLink(archive$Title_url, archive$Title))
archive$Archive_url = createLink(archive$Archive_url, archive$Archive_url)
archive2 = archive[, c(1,2,3,5)]

write.csv(archive2, "archive2.csv", row.names = F)
