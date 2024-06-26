(define (problem FreeCell3-4)
(:domain freecell)
(:objects
	diamond club heart spade 
	N0 N1 N2 N3 N4 N5 
	spade3
	club2
	spade2
	clubA
	heart3
	heart2
	diamond3
	club3
	diamondA
	diamond2
	heartA
	spadeA
	diamond0
	club0
	heart0
	spade0
	
)
(:init
	(successor N1 N0)
	(successor N2 N1)
	(successor N3 N2)
	(successor N4 N3)
	(successor N5 N4)
	(jokercard diamond3)
	(jokercard heart3)
	(jokercard club3)
	(jokercard spade3)
	(cellspace N2)
	(clear spade3)
	(on spade3 heart2)
	(on heart2 heartA)
	(bottomcol heartA)
	(clear club2)
	(on club2 diamond3)
	(on diamond3 spadeA)
	(bottomcol spadeA)
	(clear spade2)
	(on spade2 club3)
	(bottomcol club3)
	(clear clubA)
	(on clubA diamondA)
	(bottomcol diamondA)
	(clear heart3)
	(on heart3 diamond2)
	(bottomcol diamond2)
	(colspace N0)
	(value spade3 N3)
	(suit spade3 spade)
	(value club2 N2)
	(suit club2 club)
	(value spade2 N2)
	(suit spade2 spade)
	(value clubA N1)
	(suit clubA club)
	(value heart3 N3)
	(suit heart3 heart)
	(value heart2 N2)
	(suit heart2 heart)
	(value diamond3 N3)
	(suit diamond3 diamond)
	(value club3 N3)
	(suit club3 club)
	(value diamondA N1)
	(suit diamondA diamond)
	(value diamond2 N2)
	(suit diamond2 diamond)
	(value heartA N1)
	(suit heartA heart)
	(value spadeA N1)
	(suit spadeA spade)
	(home diamond0)
	(value diamond0 N0)
	(suit diamond0 diamond)
	(home club0)
	(value club0 N0)
	(suit club0 club)
	(home heart0)
	(value heart0 N0)
	(suit heart0 heart)
	(home spade0)
	(value spade0 N0)
	(suit spade0 spade)
)
(:goal (and
	(home diamond3)
	(home club3)
	(home heart3)
	(home spade3)
)))
