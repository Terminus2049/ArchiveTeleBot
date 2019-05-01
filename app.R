
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
    DT::datatable(archive2, escape = FALSE,
                  options = list(pageLength = 30))
  })

}

shinyApp(ui, server)
