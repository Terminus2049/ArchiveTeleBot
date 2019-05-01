
library(shiny)
library(readr)

createLink <- function(link, text) {
  paste0('<a href="', link,
             '" target="_blank" class="btn btn-primary">', text, '</a>')
}


ui <- function(input, output, session){

  navbarPage(
    title = 'ArchiveTeleBot',
    tabPanel('自动检查（每1h更新一次）',
             DT::dataTableOutput("table1")
    )
  )
}


server <- function(input, output, session) {

  archive2 = reactiveFileReader(60000, session, 'archive2.csv', read_csv)
  output$table1 <- DT::renderDataTable({

    archive2 = archive2()
    archive2$Title = ifelse(nchar(archive2$Title) > 10, substr(archive2$Title, 1, 20), archive2$Title)
    archive2$Title_url = ifelse(startsWith(archive2$Title_url, "https://mp.weixin.qq.com/s"),
                               archive2$Title,
                               createLink(archive2$Title_url, archive2$Title))
    archive2$Archive_url = createLink(archive2$Archive_url, archive2$Archive_url)
    DT::datatable(archive2[, c(1,2,3,5)], escape = FALSE,
                  options = list(pageLength = 30))
  })

}

shinyApp(ui, server)
