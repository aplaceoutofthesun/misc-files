sumArray=function(x,y) {
  if (x == 0 && y == 0) { #condition in c
    return(0)
  } else if (x+y == 0) { #condition in b
    print("warning x+y=0")
  }else {
    ((x^2+y^2)/(x+y))
  }
}


sumArray(0,0)

