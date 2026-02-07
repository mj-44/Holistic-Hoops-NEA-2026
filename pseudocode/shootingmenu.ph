CLASS ShootingMenu INHERITS FROM Frame
    
    FUNCTION __init__(parent, controller)
        CALL parent constructor WITH parent, background_color = BG_COLOUR
        SET this.controller TO controller

        SET main_frame TO create_frame(this)
        PLACE main_frame AT relative_x = 0.5, relative_y = 0.5, anchor = "center"

        SET title TO NEW StyledLabel(
            main_frame,
            text = "Shooting Menu",
            size = 21,
            bold = TRUE
        )
        PACK title WITH vertical_padding = (0, 50)

        SET around_the_world_button TO NEW ButtonStyle(
            main_frame,
            text = "Around the World",
            command = LAMBDA FUNCTION: controller.show_page("AroundTheWorld"),
            width = 20
        )
        PACK around_the_world_button WITH vertical_padding = 10

        SET dribble_pullup_button TO NEW ButtonStyle(
            main_frame,
            text = "Dribble Pull-Up",
            command = LAMBDA FUNCTION: controller.show_page("DribblePullUpDrill"),
            width = 20
        )
        PACK dribble_pullup_button WITH vertical_padding = 10

        SET range_rumble_button TO NEW ButtonStyle(
            main_frame,
            text = "Range Rumble",
            command = LAMBDA FUNCTION: controller.show_page("RangeRumble"),
            width = 20
        )
        PACK range_rumble_button WITH vertical_padding = 10

        SET backButton TO NEW ButtonStyle(
            main_frame,
            text = "Back to Training Menu",
            command = LAMBDA FUNCTION: controller.show_page("TrainingMenu"),
            width = 20
        )
        PACK backButton WITH vertical_padding = 10
    END FUNCTION
    
END CLASS