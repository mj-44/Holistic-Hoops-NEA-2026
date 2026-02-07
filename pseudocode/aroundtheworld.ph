CLASS AroundTheWorld INHERITS FROM Frame
    
    FUNCTION __init__(parent, controller)
        CALL parent constructor WITH parent, background_color = BG_COLOUR
        SET this.controller TO controller

        SET this.makes TO 0
        SET this.misses TO 0
        SET this.total_shots TO 50

        SET main_frame TO create_frame(this)
        PLACE main_frame AT relative_x = 0.5, relative_y = 0.5, anchor = "center"

        SET title TO NEW StyledLabel(
            main_frame,
            text = "Around The World Drill",
            size = 21,
            bold = TRUE
        )
        PACK title WITH vertical_padding = (0, 20)

        SET subtitle TO NEW StyledLabel(
            main_frame,
            text = "Drill Focused on 3s around the perimeter!",
            size = 14,
            bold = FALSE
        )
        PACK subtitle WITH vertical_padding = (0, 20)

        SET drillImage TO OPEN IMAGE("assets/around_the_world_drill.png")
        SET drillImage TO RESIZE drillImage TO (500, 300) WITH LANCZOS
        SET this.drillPhoto TO CONVERT drillImage TO PhotoImage

        SET imageLabel TO NEW Label(main_frame, image = this.drillPhoto, background_color = BG_COLOUR)
        PACK imageLabel WITH vertical_padding = (0, 20)

        SET instructionsLabel TO NEW StyledLabel(
            main_frame,
            text = "Instructions:",
            size = 16,
            bold = TRUE
        )
        PACK instructionsLabel WITH vertical_padding = (20, 10)

        SET steps TO [
            "1. Start at the corner and take a 10 3-point shots",
            "2. Move to the next spot along the perimeter after attempting 10 shots",
            "3. Go to all 5 spots around the perimeter",
            "4. Get a score out of 50 (10 shots from each spot)"
        ]

        FOR EACH step IN steps DO
            SET stepLabel TO NEW StyledLabel(
                main_frame,
                text = step,
                size = 12,
                bold = FALSE
            )
            PACK stepLabel WITH vertical_padding = 5, horizontal_padding = 40, anchor = "w"
        END FOR

        SET scoreFrame TO create_frame(main_frame)
        PACK scoreFrame WITH vertical_padding = 30

        SET this.scoreLabel TO NEW StyledLabel(
            scoreFrame,
            text = "Score: " + this.makes + "/" + (this.makes + this.misses),
            size = 20,
            bold = TRUE
        )
        PACK this.scoreLabel WITH vertical_padding = 10

        SET this.progressLabel TO NEW StyledLabel(
            scoreFrame,
            text = "Shots Taken: " + (this.makes + this.misses) + "/" + this.total_shots,
            size = 14,
            bold = FALSE
        )
        PACK this.progressLabel WITH vertical_padding = 5

        SET this.percentageLabel TO NEW StyledLabel(
            scoreFrame,
            text = "Shooting Percentage: 0.0%",
            size = 14,
            bold = FALSE
        )
        PACK this.percentageLabel WITH vertical_padding = 5

        SET buttonContainer TO create_frame(main_frame)
        PACK buttonContainer WITH vertical_padding = 20

        SET this.makeButton TO NEW ButtonStyle(
            buttonContainer,
            text = "MAKE",
            command = this.record_make,
            width = 12
        )
        PACK this.makeButton WITH side = "left", horizontal_padding = 10

        SET this.missButton TO NEW ButtonStyle(
            buttonContainer,
            text = "MISS",
            command = this.record_miss,
            width = 12
        )
        PACK this.missButton WITH side = "left", horizontal_padding = 10

        SET backButton TO NEW ButtonStyle(
            main_frame,
            text = "Back",
            command = LAMBDA FUNCTION: controller.show_page("ShootingMenu"),
            width = 20
        )
        PACK backButton WITH vertical_padding = 10

        SET resetButton TO NEW ButtonStyle(
            main_frame,
            text = "Reset Drill",
            command = this.reset_drill,
            width = 12
        )
        PACK resetButton WITH side = "left", vertical_padding = 10
    END FUNCTION

    FUNCTION record_make()
        IF this.makes + this.misses >= this.total_shots THEN
            SHOW MESSAGE BOX("Drill Complete", "You have completed all 50 shots!")
            RETURN
        END IF

        SET this.makes TO this.makes + 1
        CALL this.update_display()

        IF this.makes + this.misses >= this.total_shots THEN
            CALL this.drill_complete()
        END IF
    END FUNCTION

    FUNCTION record_miss()
        IF this.makes + this.misses >= this.total_shots THEN
            SHOW MESSAGE BOX("Drill Complete", "You have completed all 50 shots!")
            RETURN
        END IF
        
        SET this.misses TO this.misses + 1
        CALL this.update_display()

        IF this.makes + this.misses >= this.total_shots THEN
            CALL this.drill_complete()
        END IF
    END FUNCTION

    FUNCTION update_display()
        CONFIGURE this.scoreLabel WITH text = "Score: " + this.makes + "/" + (this.makes + this.misses)
        SET shots_taken TO this.makes + this.misses
        CONFIGURE this.progressLabel WITH text = "Shots Taken: " + shots_taken + "/" + this.total_shots

        IF shots_taken > 0 THEN
            SET percentage TO (this.makes / shots_taken) * 100
            CONFIGURE this.percentageLabel WITH text = "Shooting %: " + percentage + "%"
        ELSE
            CONFIGURE this.percentageLabel WITH text = "Shooting %: 0.0%"
        END IF
    END FUNCTION

    FUNCTION drill_complete()
        SET percentage TO (this.makes / this.total_shots) * 100
        
        SET message TO "Drill Complete!" + NEWLINE + NEWLINE + "Final Score: " + this.makes + "/" + this.total_shots + NEWLINE + "Shooting Percentage: " + percentage + "%"
        SHOW MESSAGE BOX("Drill Complete", message)

        CONFIGURE this.makeButton WITH state = "disabled"
        CONFIGURE this.missButton WITH state = "disabled"
    END FUNCTION

    FUNCTION reset_drill()
        SET confirm TO SHOW YES/NO DIALOG("Reset Drill", "Are you sure you want to reset the drill? This will clear your current stats.")
        IF confirm THEN
            SET this.makes TO 0
            SET this.misses TO 0
            CALL this.update_display()
            CONFIGURE this.makeButton WITH state = "normal"
            CONFIGURE this.missButton WITH state = "normal"
        END IF
    END FUNCTION

    FUNCTION tkraise(aboveThis = NULL)
        CALL parent tkraise WITH aboveThis
        CALL this.reset_drill()
    END FUNCTION
    
END CLASS

