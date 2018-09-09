
library(shiny)
library(readr)

createLink <- function(link, text) {
  l = paste0('<a href="', link,
             '" target="_blank" class="btn btn-primary">', text, '</a>')
  sprintf(l, link)
}

# Define UI for data download app ----
ui <- function(input, output, session){

  navbarPage(
    title = 'ArchiveTeleBot',
    tabPanel('Check',
             DT::dataTableOutput("table1")
    )
  )
}


# Define server logic to display and download selected file ----
server <- function(input, output, session) {

  archive2 = reactiveFileReader(60000, session, 'archive2.csv', read_csv)
  output$table1 <- DT::renderDataTable({

    archive2 = archive2()
    archive2$V2 = createLink(archive2$V2, archive2$V4)
    archive2$V3 = createLink(archive2$V3, archive2$V3)
    DT::datatable(archive2[, c(1,2,3,5)], escape = FALSE)
  })

}

# Create Shiny app ----
shinyApp(ui, server)
