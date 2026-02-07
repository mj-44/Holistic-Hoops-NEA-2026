CLASS MainMenu INHERITS FROM Frame
    
    FUNCTION __init__(parent, controller)
        CALL parent constructor WITH parent, background_color = BG_COLOUR
        SET this.controller TO controller

        SET main_frame TO create_frame(this)
        PLACE main_frame AT relative_x = 0.5, relative_y = 0.5, anchor = "center"

        SET title TO NEW StyledLabel(
            main_frame,
            text = "Hollistic Hoops",
            size = 21,
            bold = TRUE
        )
        PACK title WITH vertical_padding = (0, 50)

        SET trainingButton TO NEW ButtonStyle(
            main_frame,
            text = "Training",
            command = LAMBDA FUNCTION: controller.show_page("TrainingMenu"),
            width = 15
        )
        PACK trainingButton WITH vertical_padding = 10

        SET settingsButton TO NEW ButtonStyle(
            main_frame,
            text = "Settings",
            command = LAMBDA FUNCTION: controller.show_page("SettingsPage"),
            width = 15
        )
        PACK settingsButton WITH vertical_padding = 10

        SET trackerButton TO NEW ButtonStyle(
            main_frame,
            text = "Tracker",
            command = LAMBDA FUNCTION: controller.show_page("TrackingPage"),
            width = 15
        )
        PACK trackerButton WITH vertical_padding = 10

        SET comparisonButton TO NEW ButtonStyle(
            main_frame,
            text = "Comparison",
            command = LAMBDA FUNCTION: controller.show_page("ComparisonPage"),
            width = 15
        )
        PACK comparisonButton WITH vertical_padding = 10
    END FUNCTION
    
END CLASS