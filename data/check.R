
library(shiny)
library(readr)

createLink <- function(link, text) {
  l = paste0('<a href="', link,
             '" target="_blank" class="btn btn-primary">', text, '</a>')
  sprintf(l, link)
}


ui <- function(input, output, session){

  navbarPage(
    title = 'ArchiveTeleBot',
    tabPanel('Check',
             DT::dataTableOutput("table1")
    )
  )
}


server <- function(input, output, session) {

  archive2 = reactiveFileReader(60000, session, 'archive2.csv', read_csv)
  output$table1 <- DT::renderDataTable({

    archive2 = archive2()
    names(archive2) = c('Time', 'Title_url', 'Archive_url', 'Title', 'Check')
    archive2$Time = substr(archive2$Time, 5, nchar(archive2$Time))
    archive2$Time = parse_datetime(archive2$Time, format = "%b %d %H:%M:%S %Y")
    archive2$Time = archive2$Time + 8*60*60
    archive2$Title_url = createLink(archive2$Title_url, archive2$Title)
    archive2$Archive_url = createLink(archive2$Archive_url, archive2$Archive_url)
    DT::datatable(archive2[, c(1,2,3,5)], escape = FALSE)
  })

}

shinyApp(ui, server)
