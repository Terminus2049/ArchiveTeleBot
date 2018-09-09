
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
    tabPanel('实时查看',
             DT::dataTableOutput("table0")
    ),
    tabPanel('自动检查（每6h更新一次）',
             DT::dataTableOutput("table1")
    )
  )
}


server <- function(input, output, session) {

  archive = reactiveFileReader(60000, session, 'archive.csv', read_csv)
  output$table0 <- DT::renderDataTable({

    archive = archive()
    names(archive) = c('Time', 'Title_url', 'Archive_url', 'Title')
    archive$Time = substr(archive$Time, 5, nchar(archive$Time))
    archive$Time = parse_datetime(archive$Time, format = "%b %d %H:%M:%S %Y")
    archive$Time = archive$Time + 8*60*60
    archive$Title_url = createLink(archive$Title_url, archive$Title)
    archive$Archive_url = createLink(archive$Archive_url, archive$Archive_url)
    DT::datatable(archive[, 1:3], escape = FALSE)
  })

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
