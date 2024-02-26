;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; FreeCellWorld
;;; Free cell game playing domain
;;;
;;; Description
;;; ------------
;;; Freecell is a solitaire game that comes with Windows.
;;; If you haven't seen it before:
;;;  One has 8 columns of cards, 4 freecells and 4 homecells. The
;;;  cards start in "random" (random according to MS's brain damaged RNG)
;;;  piles in the 8 columns. We can move a card in the following ways: 
;;;  1. we can move any card that is on top of a column to an empty free
;;;     cell. The free cells only take one card each.
;;;  2. we can move any card from a free cell or from top of a column to
;;;  a home cell if that home cell contains a card of the same suit
;;;  and is one lower in value (aces have value 1, Jacks 11, Queens
;;;  12, Kings 13, and to make things more symmetric we start the
;;;  homecells off containing "phone" cards with value 0.
;;;  3. we can move any card from the  top of a column or from a
;;;  freecell to the top of another column if that column currently holds
;;;  a card with an opposite colour suit that has one higher
;;;  value. 
;;;  4. we can move any card from a free cell or on top of a column to a
;;;  new column if there are less than 8 columns.
;;;
;;; The aim is to get all of the card home. 
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Cards are represented by the symbols 
;;;		ca, c2, ..., cj, cq, ck. - clubs
;;;		da, d2, ..., dj, dq, dk. - diamonds
;;;		ha, h2, ..., hj, hq, gk. - hearts
;;;		sa, s2, ..., sj, sq, sk. - spaces
;;;		(c0, d0, h0, s0 indicate an empty card of a certain suit).
;;; 
;;; Where:
;;;		c = clubs, d = diamonds, h = hearts, s = spades.
;;;		a = ace, j = jack, q = queen, k = king.
;;;
;;; Static Predicates (In Tlplan these were functions)
;;; 
;;; (value card val)   --- the face value of the card. (1, ..., 13)
;;; (suit card st)     --- the suit of the card. (c, d, h, s)
;;;   e.g., (value ca 1) (suit ca c)
;;; (successor n' n)   --- n' = n+1, for n=0,...,12, n'=1,...,13
;;;                        a cheap and dirty way to avoid using
;;;                        numbers. 
;;;                        Note 0 does not have a predecessor. This
;;;                        serves act as > 0 precondition
;;;
;;;
;;; Dynamic Predicates:
;;;
;;; (on card1 card2)	-- card1 is on card2
;;; (incell card)	--- card is in a freecell.
;;; (clear card)	--- card is clear (i.e., on top of a column).
;;; (cellspace n)	--- there are n free freecells.
;;;                                n = 0, 1, 2, 3, or 4
;;; (colspace n)	--- there are n free columns. n=0,..,8
;;; (home card)		--- card is a top card in a home stack.
;;;			    we use the special (home c0),
;;;			    (home d0), (home h0), (home s0).
;;;			    to indicate that home is empty for a
;;;			    particular suit.
;;; (bottomcol card)	--  card is at the bottom of a stack.
;;; (jokercard card)    -- the card is a joker card and thus can be added to the home colum if no
;;;						   other cards are on top of it based on its suite.
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain freecell)
  (:requirements :strips :disjunctive-preconditions) 
  (:predicates (on ?c1 ?c2)
	       (incell ?c)
	       (clear ?c)
	       (cellspace ?n)
	       (colspace ?n)
	       (home ?c)
	       (bottomcol ?c)
	       (suit ?c ?s)
	       (value ?c ?v)
	       (successor ?n1 ?n0)
	       (jokercard ?c)
 )

;;; Move card between columns. Two versions dependent on whether or
;;; not we generate a new stack.

  (:action move
	   :parameters (?card ?oldcard ?newcard)
	   :precondition (and (clear ?card) 
			      (clear ?newcard)
			      (on ?card ?oldcard))
	   :effect (and (on ?card ?newcard)
	   		(not (clear ?newcard))
			(clear ?oldcard)
			(not (on ?card ?oldcard))))

  (:action move-b
	   :parameters (?card ?newcard ?cols ?ncols)
	   :precondition (and (clear ?card) 
			      (bottomcol ?card)
			      (clear ?newcard)
			      (colspace ?cols)
			      (successor ?ncols ?cols))
	   :effect (and (on ?card ?newcard)
			(colspace ?ncols)
			(not (bottomcol ?card))
			(not (clear ?newcard))
			(not (colspace ?cols))))

;; Send a card to a freecell. Two versions dependent on whether or not
;; we generate a new stack.

  (:action sendtofree 
	   :parameters (?card ?oldcard ?cells ?ncells)
	   :precondition (and (clear ?card)
				(on ?card ?oldcard)
				(successor ?cells ?ncells)
				(cellspace ?cells))
	   :effect (and (incell ?card)
			(cellspace ?ncells)
			(clear ?oldcard)
			(not (clear ?card))
			(not (cellspace ?cells))
			(not (on ?card ?oldcard))))

  (:action sendtofree-b 
	   :parameters (?card ?cells ?ncells ?cols ?ncols)
	   :precondition (and (clear ?card)
	   				(successor ?cells ?ncells)
					(successor ?ncols ?cols)
					(bottomcol ?card)
					(cellspace ?cells)
					(colspace ?cols))
	   :effect (and (incell ?card)
	   		(not (clear ?card))
			(cellspace ?ncells)
			(colspace ?ncols)
			(not (cellspace ?cells))
			(not (colspace ?cols))
			(not (bottomcol ?card))))

;; Send a card a new column

(:action sendtonewcol
	 :parameters (?card ?oldcard ?cols ?ncols)
	 :precondition (and (clear ?card)
	 		(on ?card ?oldcard)
	 		(colspace ?cols)
			(successor ?cols ?ncols))
	 :effect (and (clear ?oldcard)
	 		(not (colspace ?cols))
			(colspace ?ncols)
			(bottomcol ?card)
			(not (on ?card ?oldcard))))
			

;;Send a card home

(:action sendtohome
	 :parameters (?card ?oldcard ?suit ?vcard ?homecard ?vhomecard)
	 :precondition (and
			(clear ?card) 
			(on ?card ?oldcard)
			(home ?homecard)
			(suit ?card ?suit)
			(suit ?homecard ?suit)
			(value ?card ?vcard)
			(or (successor ?vcard ?vhomecard)
				(jokercard ?card))
			(value ?homecard ?vhomecard))
	 :effect (and (home ?card)
		      (clear ?oldcard)
		      (not (on ?card ?oldcard))
			  (not (home ?homecard))))

(:action sendtohome-b
	 :parameters (?card ?suit ?vcard ?homecard
			    ?vhomecard ?cols ?ncols)
	 :precondition (and 
	 			(clear ?card)
				(colspace ?cols)
				(bottomcol ?card)
				(home ?homecard)
				(suit ?card ?suit)
				(suit ?homecard ?suit)
				(value ?card ?vcard)
				(successor ?ncols ?cols)
				(or (successor ?vcard ?vhomecard)
					(jokercard ?card))
				(value ?homecard ?vhomecard))
	 :effect (and (home ?card)
	 			(colspace ?ncols)
				(not (colspace ?cols))
				(not (home ?homecard))
				(not (bottomcol ?card))))
				

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Move cards in free cell
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(:action homefromfreecell
	 :parameters (?card ?suit ?vcard
			    ?homecard ?vhomecard ?cells ?ncells)
    ;;Send a card home from a free cell.
	 :precondition (and (incell ?card)
				(cellspace ?cells)
				(home ?homecard)
				(suit ?card ?suit)
				(suit ?homecard ?suit)
				(value ?card ?vcard)
				(or (successor ?vcard ?vhomecard)
					(jokercard ?card))
				(value ?homecard ?vhomecard)
				(successor ?ncells ?cells))
	 :effect (and (home ?card)
				(cellspace ?ncells)
				(not (home ?homecard))
				(not (incell ?card))
				(not (cellspace ?cells))))

(:action colfromfreecell
	 :parameters (?card ?newcard ?cells ?ncells)
	 :precondition (and (incell ?card)
				(clear ?newcard)
				(cellspace ?cells)
				(successor ?ncells ?cells))
	 :effect (and (clear ?card)
	 			(not (clear ?newcard))
				(on ?card ?newcard)
				(cellspace ?ncells)
				(not (cellspace ?cells))
				(not (incell ?card))))

(:action newcolfromfreecell
	 :parameters (?card ?cols ?ncols ?cells ?ncells)
	 :precondition (and (incell ?card)
	 			(colspace ?cols)
				(cellspace ?cells)
				(successor ?ncells ?cells)
				(successor ?cols ?ncols))
	 :effect (and (bottomcol ?card)
	 			(clear ?card)
	 			(colspace ?ncols)
				(cellspace ?ncells)
				(not (incell ?card))
				(not (colspace ?cols))
				(not (cellspace ?cells))))

)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
