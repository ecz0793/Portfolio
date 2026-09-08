MODULE mod
    IMPLICIT NONE
	
    TYPE individu
        INTEGER, DIMENSION(2):: pos
        INTEGER, DIMENSION(2):: old_pos
        INTEGER,DIMENSION(2) :: depl
        INTEGER :: larg
        CHARACTER(LEN=1):: symbol
    END TYPE individu
	
    TYPE domaine
        INTEGER :: nl
        INTEGER :: nc
        type(individu) :: bal
        type(individu) :: raq
        LOGICAL, DIMENSION(:,:),ALLOCATABLE:: brik
        CHARACTER, DIMENSION(:,:),ALLOCATABLE:: grille
		LOGICAL, DIMENSION(:,:), ALLOCATABLE :: brik_special
    END TYPE domaine
    CONTAINS
    SUBROUTINE nb_al(nmin,nmax,res)
        INTEGER,INTENT(IN):: nmin,nmax
        REAL :: n
        REAL,INTENT(OUT):: res
        CALL RANDOM_SEED
        CALL RANDOM_NUMBER(n)
        res = nmin + (nmax-nmin) *n
    END SUBROUTINE nb_al
	
    SUBROUTINE affiche(dom)
        TYPE(domaine), INTENT(INOUT) :: dom
        INTEGER :: i, j
        DO i = 1,dom%nl
            DO j = 1, dom%nc
                dom%grille(i,j)=" "
				IF (dom%brik(i,j) .eqv. .TRUE.) THEN
					dom%grille(i,j) ="X"
				END IF
				IF (dom%brik_special(i,j) .eqv. .TRUE.)THEN
					dom%grille(i,j) = "2"
				END IF
            END DO
        END DO
		
        DO i = 1, dom%nl
            dom%grille(i,0)="|"
            dom%grille(i,dom%nc+1)="|"
        END DO
        DO j = 0, dom%nc+1
            dom%grille(0,j)="-"
        END DO
		
	!Placement de la balle 
		
        dom%grille(dom%bal%pos(1),dom%bal%pos(2)) = dom%bal%symbol
		
	! Placement de la raquette
        dom%grille(dom%raq%pos(1),:)=" "
        DO j = dom%raq%pos(2),dom%raq%pos(2)+dom%raq%larg-1
            dom%grille(dom%raq%pos(1),j) = dom%raq%symbol
        END DO
        DO i = 0,dom%nl+1
            PRINT*, dom%grille(i,:)
        END DO
    END SUBROUTINE
    SUBROUTINE deplacement_raquette(dom)
        TYPE(domaine), INTENT(INOUT) :: dom
        character:: touche
        INTEGER:: retval, tsec , tmicros
        INTEGER:: selec_get
        tsec = 0
        tmicros = 10000
        retval = selec_get(touche,tsec,tmicros)
		
		
        IF (retval == 1)THEN
            dom%raq%old_pos = dom%raq%pos
	
            SELECT CASE(touche)
                CASE("g")
                    IF (dom%raq%pos(2) > 1 )THEN
                        dom%raq%pos(2) = dom%raq%pos(2) - 1
                    END IF
                CASE("h")
                    IF (dom%raq%pos(2)+dom%raq%larg-1 < dom%nc)THEN
                        dom%raq%pos(2) = dom%raq%pos(2) + 1
                    END IF
                CASE DEFAULT
                    ! rien ne se passe
            END SELECT
        END IF
	END SUBROUTINE

	SUBROUTINE deplacement_balle(dom)
   		TYPE(domaine), INTENT(INOUT) :: dom
    		INTEGER :: x, y
    		Logical:: d,h,v,hs,vs,ds
		
    		x= dom%bal%pos(1) + dom%bal%depl(1)
    		y= dom%bal%pos(2) + dom%bal%depl(2)
    		
		IF (x <= 1) THEN
        		dom%bal%depl(1) = -dom%bal%depl(1)  
    		END IF

 
    		IF (y <= 1 .OR. y >= dom%nc) THEN
        		dom%bal%depl(2) =-dom%bal%depl(2) 
    		END IF
	
    		IF (x== dom%raq%pos(1)-1 .AND. y>= dom%raq%pos(2) .AND. y<=dom%raq%pos(2) + dom%raq%larg-1) THEN
        		dom%bal%depl(1)=-dom%bal%depl(1)  
        		
    		END IF

		dom%bal%old_pos = dom%bal%pos 
    	dom%bal%pos(1) = x
    	dom%bal%pos(2) = y


		IF (dom%bal%depl(1) == 1 .AND. dom%bal%depl(2) == 1) THEN 
			d =dom%brik(x+1,y+1)
			v =dom%brik(x+1,y)
			h =dom%brik(x,y+1)

			ds =dom%brik_special(x+1,y+1)
			vs =dom%brik_special(x+1,y)
			hs =dom%brik_special(x,y+1)

			IF (h .eqv. .TRUE.)THEN
				dom%bal%depl(2)=-dom%bal%depl(2) 
				dom%brik(x,y+1)= .FALSE. 
			
			ELSE IF (hs .eqv. .TRUE.)THEN
				dom%brik(x,y+1)= .FALSE.
				dom%bal%depl(2)=-dom%bal%depl(2)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				dom%brik_special(x,y+1)= .FALSE.

			
			ELSE IF(v .eqv. .TRUE.)THEN 
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%brik(x+1,y)  = .FALSE.

			ELSE IF(vs .eqv. .TRUE.)THEN
				dom%brik(x+1,y)  = .FALSE.
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%brik_special(x+1,y)  = .FALSE.

			
			ELSE IF (d .eqv. .TRUE.)THEN
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%bal%depl(2)=-dom%bal%depl(2) 
				dom%brik(x+1,y+1) = .FALSE.
			
			ELSE IF (ds .eqv. .TRUE.)THEN
				dom%brik(x+1,y+1) = .FALSE.
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%bal%depl(2)=-dom%bal%depl(2)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				dom%brik_special(x+1,y+1) = .FALSE.

			! deplacement brique spécial deplacement (1,1)
			END IF
		END IF
		
		IF (dom%bal%depl(1) == -1 .AND. dom%bal%depl(2) == 1) THEN 
			d =dom%brik(x-1,y+1)
			v =dom%brik(x-1,y)
			h =dom%brik(x,y+1)

			ds =dom%brik_special(x-1,y+1)
			vs =dom%brik_special(x-1,y)
			hs =dom%brik_special(x,y+1)

			IF (h .eqv. .TRUE.)THEN
				dom%bal%depl(2)=-dom%bal%depl(2)
				dom%brik(x,y+1) = .FALSE.

			ELSE IF (hs .eqv. .TRUE.)THEN
				dom%brik(x,y+1) = .FALSE.
				dom%bal%depl(2)=-dom%bal%depl(2)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')
				dom%brik_special(x,y+1) = .FALSE.
 

			ELSE IF(v .eqv. .TRUE.)THEN
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%brik(x-1,y) = .FALSE.

			ELSE IF(vs .eqv. .TRUE.)THEN
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%brik(x-1,y) = .FALSE.
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')
				dom%brik_special(x-1,y) = .FALSE.


			ELSE IF (d .eqv. .TRUE.)THEN
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%bal%depl(2)=-dom%bal%depl(2) 
				dom%brik(x-1,y+1) = .FALSE.

			ELSE IF (ds .eqv. .TRUE.)THEN
				dom%brik(x-1,y+1) = .FALSE.
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%bal%depl(2)=-dom%bal%depl(2)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')
				dom%brik_special(x-1,y+1) = .FALSE.

			END IF
		END IF
		
		IF (dom%bal%depl(1) == 1 .AND. dom%bal%depl(2) == -1) THEN 
			d =dom%brik(x+1,y-1)
			v =dom%brik(x+1,y)
			h =dom%brik(x,y-1)

			ds =dom%brik_special(x+1,y-1)
			vs =dom%brik_special(x+1,y)
			hs =dom%brik_special(x,y-1)

			IF (h .eqv. .TRUE.)THEN
				dom%brik(x,y-1) = .FALSE. 
				dom%bal%depl(2)=-dom%bal%depl(2)

			ELSE IF (hs .eqv. .TRUE.)THEN
				dom%brik(x,y-1) = .FALSE. 
				dom%brik_special(x,y-1) = .FALSE. 
				dom%bal%depl(2)=-dom%bal%depl(2)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')

			ELSE IF(v .eqv. .TRUE.)THEN
				dom%brik(x+1,y) = .FALSE. 
				dom%bal%depl(1)=-dom%bal%depl(1)

			ELSE IF(vs .eqv. .TRUE.)THEN
				dom%brik(x+1,y) = .FALSE.
				dom%brik_special(x+1,y) = .FALSE.
				dom%bal%depl(1)=-dom%bal%depl(1)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')

			ELSE IF (d .eqv. .TRUE.)THEN
				dom%brik(x+1,y-1) = .FALSE.
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%bal%depl(2)=-dom%bal%depl(2)

			ELSE IF (ds .eqv. .TRUE.)THEN
				dom%brik(x+1,y-1) = .FALSE.
				dom%brik_special(x+1,y-1) = .FALSE.
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%bal%depl(2)=-dom%bal%depl(2)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')
			END IF
		END IF
		
		IF (dom%bal%depl(1) == -1 .AND. dom%bal%depl(2) == -1) THEN 
			d =dom%brik(x-1,y-1)
			v =dom%brik(x-1,y)
			h =dom%brik(x,y-1)

			ds =dom%brik_special(x-1,y-1)
			vs =dom%brik_special(x-1,y)
			hs =dom%brik_special(x,y-1)

			IF (h .eqv. .TRUE.)THEN
				dom%brik(x,y-1) = .FALSE. 
				dom%bal%depl(2)=-dom%bal%depl(2) 

			ELSE IF (hs .eqv. .TRUE.)THEN
				dom%brik(x,y-1) = .FALSE.
				dom%brik_special(x,y-1) = .FALSE.
				dom%bal%depl(2)=-dom%bal%depl(2)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')

			ELSE IF(v .eqv. .TRUE.)THEN
				dom%brik(x-1,y) = .FALSE. 
				dom%bal%depl(1)=-dom%bal%depl(1)

			ELSE IF(vs .eqv. .TRUE.)THEN
				dom%brik(x-1,y) = .FALSE. 
				dom%brik_special(x-1,y) = .FALSE. 
				dom%bal%depl(1)=-dom%bal%depl(1)
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')
				
			ELSE IF (d .eqv. .TRUE.)THEN
				dom%brik(x-1,y-1) = .FALSE.
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%bal%depl(2)=-dom%bal%depl(2)
			
			ELSE IF (ds .eqv. .TRUE.)THEN
				dom%brik(x-1,y-1) = .FALSE.
				dom%brik_special(x-1,y-1) = .FALSE.
				dom%bal%depl(1)=-dom%bal%depl(1)
				dom%bal%depl(2)=-dom%bal%depl(2) 
				!CALL SYSTEM("timeout /t 0.1 /nobreak >nul")
				CALL SYSTEM('sleep 0.1')
			END IF
		END IF
	END SUBROUTINE deplacement_balle

END MODULE mod

PROGRAM principal
	USE mod

	IMPLICIT NONE
	type(domaine):: dom
	REAL :: random_val_x, random_val_y,s
	INTEGER:: ok,x,y,ios

	PRINT*, "Saisir le nombre de lignes de la grille"
	READ*, dom%nl
	PRINT*, "Saisir le nombre de colonnes de la grille"
	READ*, dom%nc
	!CALL system('stty cbreak')

	OPEN(UNIT=10, FILE='param.dat', STATUS='OLD', ACTION='READ', IOSTAT=ios)
    IF (ios /= 0) STOP "Erreur à l'ouverture du fichier"

	READ(10,*) dom%raq%larg  ! Largeur de la raquette
    READ(10,*) dom%bal%depl(1)  ! Direction initiale de la balle en x
    READ(10,*) dom%bal%depl(2)  ! Direction initiale de la balle en y

	CLOSE(10)

	ALLOCATE(dom%grille(0:dom%nl+1,0:dom%nc+1), stat= ok)
	IF (ok/= 0) STOP "Erreur allocation"
	
	CALL nb_al(1,dom%nc,random_val_x)
	CALL nb_al(dom%nl,dom%nl,random_val_y)
	
	!Initiailisation balle
	
	dom%bal%pos = (/random_val_y,random_val_x/)
	dom%bal%old_pos=dom%bal%pos
	!dom%bal%depl=(/-1,1/)
	dom%bal%symbol="o"
	
	!Initiailisation raquette
	
	dom%raq%pos=(/dom%nl+1, 1/)
	dom%raq%old_pos= dom%raq%pos
	!dom%raq%larg = 5
	dom%raq%symbol= "="
	
	ALLOCATE(dom%brik(0:dom%nl,0:dom%nc),stat=ok)
   	IF (ok/= 0) STOP "Erreur allocation"

	ALLOCATE(dom%brik_special(0:dom%nl,0:dom%nc),stat =ok)
	IF(ok/=0) STOp "Erreur allocation"
   	
   	!Initialisation des briques
   	Do x= 1,dom%nl/2
   		DO y=1, dom%nc
   			dom%brik(x,y) = .TRUE.
   		END DO
   		
   	END DO

	!Initialisation des briques spéciales
	Do x=1, dom%nl/2
		Do y=1, dom%nc
			CALL RANDOM_NUMBER(s)
			IF (s < 0.2)THEN
				dom%brik_special(x,y) = .TRUE.
				dom%brik(x,y)= .FALSE.
			END IF
		END DO
	END DO

	Do x= dom%nl/2 + 1,dom%nl
   		DO y=1, dom%nc
   			dom%brik(x,y) = .FALSE.
			dom%brik_special(x,y) = .FALSE.
   		END DO
   		
   	END DO
	 

	!Initialisation des briques spéciales
	Do x=1, dom%nl/2
		Do y=1, dom%nc
			CALL RANDOM_NUMBER(s)
			Print*, s
			IF (s < 0.1)THEN		! Chance d'apparition
				dom%brik_special(x,y) = .TRUE.
			END IF
		END DO
	END DO

	CALL affiche(dom)
	DO
		!CALL SYSTEM('sleep 0.2') !(Sous Linux/MacOS)
		CALL SYSTEM("timeout /t 0 /nobreak >nul") !(Sous Windows)
		!CALL SYSTEM('clear') !(Sous Linux/MacOS)
		CALL SYSTEM('cls') !(Sous Windows)
		CALL deplacement_raquette(dom)
		CALL deplacement_balle(dom)
		CALL affiche(dom)
		IF (dom%bal%pos(1) >= dom%nl+1)THEN
			PRINT*, "Vous avez perdu !"
			EXIT
		END IF
	END DO
	!CALL system('stty -cbreak') !(Linux)
 
END PROGRAM principal

