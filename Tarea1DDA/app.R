#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

#Importar librerias necesarias
library(docstring)
library(ggplot2)
library(shiny)

#### ALGORITMO DDA ####
dda <- function(x0, y0, x1, y1){
  #' Crea lineas siguiendo el algoritmo DDA
  #'
  #' @param x0,y0 coordenadas del punto inicial de la linea
  #' @param x1,y1 coordenadas del punto final de la linea
  #' REGRESA:
  #' Un dataframe con todas las coordenadas
  #'
  #' Hecho con amor
  
  #Declaramos un vector vacio para guardar las coordenadas
  coords <- c()
  
  #Calculamos las pendientes
  mx <- x1 - x0
  my <- y1 - y0
  
  #Determinamos el tamanio del paso
  s <- if ( abs(mx) > abs(my) ) abs(mx)  else abs(my)
  
  #Calculamos el incremento para cada direccion
  dx <- mx/s
  dy <- my/s
  
  #Iniciamos las variables xk y yk
  xk <- x0
  yk <- y0
  
  #Agregamos xy y yk a las coordenadas
  coords <- rbind(coords, c(round(xk), round(yk)) )
  
  #Hacemos los pasos necesarios
  
  for (i in 1:s) {
    #Incrementamos xk y yk
    xk <- xk + dx
    yk <- yk + dy
    #Agregamos xy y yk a las coordenadas
    coords <- rbind(coords, c(round(xk), round(yk)) )
    
  }
  
  #Convertimos la lista a un dataframe
  coords <- as.data.frame(coords)
  #Renombramos las columnas
  names(coords) <- c("x", "y")
  #Regresamos el dataframe
  return(coords)
}


#### ALGORITMO BRESENHAM ####
bresenham <- function(x0, y0, x1, y1){
  #' Crea lineas siguiendo el algoritmo de Bresenham
  #'
  #' @param x0,y0 coordenadas del punto inicial de la linea
  #' @param x1,y1 coordenadas del punto final de la linea
  #' REGRESA:
  #' Un dataframe con todas las coordenadas
  #'
  #' Hecho con amor
  #Declaramos un vector vacio para guardar las coordenadas
  coords <- c()
  
  #Iniciamos las variables xk y yk
  xk <- x0
  yk <- y0
  
  #Agregamos xy y yk a las coordenadas
  coords <- rbind(coords, c(round(xk), round(yk)) )
  
  #Calculamos las diferencias
  dx <- x1 - x0
  dy <- y1 - y0
  
  #Determinamos el parametro decisivo
  pk <- 2*dy - dx
  
  #Mientras no lleguemos a x1 seguimos agregando puntos
  
  while ( xk<=x1 & yk<=y1) {
    
    #Nos movemos en el eje x
      xk <- xk +1
    
    #Revisamos el signo de pk
    if (pk<=0){
      pk <- pk + 2*dy
    }
    else{
      yk <- yk + 1
      pk <- pk + 2*dy - 2*dx
    }
    
    #Agregamos xy y yk a las coordenadas
    coords <- rbind(coords, c(xk, yk) )
    
  }
  
  #Convertimos la lista a un dataframe
  coords <- as.data.frame(coords)
  #Renombramos las columnas
  names(coords) <- c("x", "y")
  #Regresamos el dataframe
  return(coords)
}

#### APLICACION ####

#Controles para puntos
## Lineas
 p0_control <- fixedRow(
  helpText("Punto Inical"),
  column( width = 3,
          numericInput(
            "x0",withMathJax("$$x_0$$"),
            value=13
          )
  ),
  column( width = 3,
          numericInput(
            "y0", withMathJax("$$y_0$$"),
            value=18
          )
  )
)
 
p1_control <- fixedRow(
  helpText("Punto Final"),
  column( width = 3,
          numericInput(
            "x1", withMathJax("$$x_1$$"),
            value=19
          )
  ),
  column( width = 3,
          numericInput(
            "y1", withMathJax("$$y_1$$"),
            value=89
          )
  )
)

## Triangulo
v0_control <- fixedRow(
  helpText("Vértice A"),
  column( width = 3,
          numericInput(
            "xA",withMathJax("$$x_A$$"),
            value=13
          )
  ),
  column( width = 3,
          numericInput(
            "yA", withMathJax("$$y_A$$"),
            value=18
          )
  )
)

v1_control <- fixedRow(
  helpText("Vértice B"),
  column( width = 3,
          numericInput(
            "xB", withMathJax("$$x_B$$"),
            value=19
          )
  ),
  column( width = 3,
          numericInput(
            "yB", withMathJax("$$y_B$$"),
            value=89
          )
  )
)


v2_control <- fixedRow(
  helpText("Vértice C"),
  column( width = 3,
          numericInput(
            "xC", withMathJax("$$x_C$$"),
            value=25
          )
  ),
  column( width = 3,
          numericInput(
            "yC", withMathJax("$$y_C$$"),
            value=22
          )
  )
)

#Seleccion de algoritmo
alg_control <- fixedRow(
  selectInput("algo", "Algoritmo",
              choices = c(
                "Digital Differential Analyzer (DDA)"="dda",
                "Bresenham"= "bresenham"
              ),
              selected = "dda"
  )
)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Trazado de lineas"),
    helpText("Creado por Jazmín López Chacón"),
    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            tabsetPanel( type="tabs", id="tab",
              tabPanel("Línea", value="linea",
              p0_control,
              p1_control,
              alg_control
              ),
              tabPanel("Triángulo", value="triangulo",
                v0_control,
                v1_control,
                v2_control
              )
            )
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("scatterPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  output$scatterPlot <- renderPlot({
  
  #Revisamos en que pestania estamos
  tab <- input$tab
  
  #Color vertices
  vcolor <- "#4293ff"
  
  if(tab=="linea"){
    #Tomamos los valores insertados  
    x0 <- round(input$x0)
    y0 <- round(input$y0)
    x1 <- round(input$x1)
    y1 <- round(input$y1)
    algo <- input$algo
    if (algo=="bresenham"){
      coords <- bresenham(x0,y0,x1,y1)
      algoritmo <- "Bresenham"
    }
    else{
      coords <- dda(x0,y0,x1,y1)
      algoritmo <- "DDA"
    }
    
    #Etiquetas de vertices
    vertices <- geom_point(aes(x=c(x0,x1),y=c(y0,y1)), size=5, colour=vcolor)
    etiquetas <- geom_text(aes(x=c(x0,x1),y=c(y0,y1)), size=5, colour=vcolor, label=c("A","B"), vjust = -0.5)
  }
  else{
    #Tomamos los valores insertados  
    x0 <- round(input$xA)
    y0 <- round(input$yA)
    x1 <- round(input$xB)
    y1 <- round(input$yB)
    x2 <- round(input$xC)
    y2 <- round(input$yC)
    
    #A-B
    coords <- dda(x0,y0,x1,y1)
    #B-C
    coords <- rbind(coords,dda(x1,y1,x2,y2))
    #C-A
    coords <- rbind(coords,dda(x2,y2,x0,y0))
    algoritmo <- "DDA"
    
    #Vertices
    vertices <- geom_point(aes(c(x0,x1,x2), c(y0,y1,y2)), size=5, colour=vcolor)
    etiquetas <- geom_text(aes(c(x0,x1,x2), c(y0,y1,y2)), label=c("A","B", "C"), size=5, colour=vcolor,  vjust = -0.5)
  }

  #Plot de los pixeles con centro en la coordenada y tamanio 1x1
  fcolor <- "#FFAE42"
  ggplot()+
    geom_tile(data=coords,mapping=aes(x,y),fill=fcolor)+
    vertices+etiquetas+
    labs(x="x", y="y",
         title="Creación de líneas",
         subtitle = paste("Algoritmo",algoritmo),
         caption="Nota: Elaboración propia (2023)")+
    theme_minimal()
})
}

# Run the application 
shinyApp(ui = ui, server = server)
