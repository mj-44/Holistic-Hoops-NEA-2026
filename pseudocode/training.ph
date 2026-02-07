CLASS TrainingMenu INHERITS FROM Frame
    
    FUNCTION __init__(parent, controller)
        CALL parent constructor WITH parent, background_color = BG_COLOUR
        SET this.controller TO controller

        SET main_frame TO create_frame(this)
        PLACE main_frame AT relative_x = 0.5, relative_y = 0.5, anchor = "center"

        SET title TO NEW StyledLabel(
            main_frame,
            text = "Training Menu",
            size = 21,
            bold = TRUE
        )
        PACK title WITH vertical_padding = (0, 50)

        SET shootingButton TO NEW ButtonStyle(
            main_frame,
            text = "Shooting",
            command = LAMBDA FUNCTION: controller.show_page("ShootingMenu"),
            width = 20
        )
        PACK shootingButton WITH vertical_padding = 10

        SET dribblingButton TO NEW ButtonStyle(
            main_frame,
            text = "Dribbling",
            command = LAMBDA FUNCTION: controller.show_page("DribblingMenu"),
            width = 20
        )
        PACK dribblingButton WITH vertical_padding = 10

        SET footworkButton TO NEW ButtonStyle(
            main_frame,
            text = "Footwork",
            command = LAMBDA FUNCTION: controller.show_page("FootworkMenu"),
            width = 20
        )
        PACK footworkButton WITH vertical_padding = 10

        SET finishingButton TO NEW ButtonStyle(
            main_frame,
            text = "Finishing",
            command = LAMBDA FUNCTION: controller.show_page("FinishingMenu"),
            width = 20
        )
        PACK finishingButton WITH vertical_padding = 10
        
        SET backButton TO NEW ButtonStyle(
            main_frame,
            text = "Back to Main Menu",
            command = LAMBDA FUNCTION: controller.show_page("MainMenu"),
            width = 20
        )
        PACK backButton WITH vertical_padding = 30
    END FUNCTION
    
END CLASS