CLASS BasketballApp
    
    FUNCTION __init__()
        SET this.root TO NEW Window()
        SET WINDOW TITLE TO "Hollistic Hoops"
        
        SET WINDOW GEOMETRY TO "720x1280"
        SET WINDOW RESIZABLE TO FALSE, FALSE
        
        CONFIGURE this.root WITH background_color = "#000000"
        
        CALL initialise_database()
        
        SET this.container TO NEW Frame(this.root, background_color = "#000000")
        PACK this.container WITH fill = "both", expand = TRUE
        
        SET this.pages TO EMPTY DICTIONARY
        
        FOR EACH PageClass IN (HomePage, LoginPage, RegisterPage, ForgotPasswordPage, MainMenu, TrainingMenu, 
        ShootingMenu, DribblingMenu, FootworkMenu, FinishingMenu, DribblePullUpDrill, AlleyDrill, AroundTheWorld, 
        BackPedalFinishing, BackPedalFinishingPF, ConeTouchFinishing, FresnoAttack, OffBalancePullUps, RangeRumble) DO
            SET page_name TO PageClass.__name__
            SET page TO NEW PageClass(parent = this.container, controller = this)
            SET this.pages[page_name] TO page
            PLACE page AT relative_x = 0, relative_y = 0, relative_width = 1, relative_height = 1
        END FOR
        
        CALL this.show_page("HomePage")
    END FUNCTION
    
    FUNCTION show_page(page_name)
        SET page TO this.pages[page_name]
        RAISE page TO FRONT
    END FUNCTION
    
    FUNCTION run()
        START MAINLOOP ON this.root
    END FUNCTION
    
END CLASS

IF MAIN PROGRAM THEN
    SET app TO NEW BasketballApp()
    CALL app.run()
END IF