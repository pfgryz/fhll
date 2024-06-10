from src.interpreter.interpreter import Interpreter
from tests.interpreter.helpers import load_module


def test_interpreter_e2e():
    module = load_module("""
    struct List {}
    enum Result {
        struct Err {};
        struct Ok {
            value: UI::Window;
        };
    }
    
    fn sleep(x: i32) {}
    fn create_main_window() {}
    fn create_component(n: str) -> UI::Component {
        return UI::Component::Button{};
    }
    fn get_main_window() -> UI::Window {
        return UI::Window {
            name = "Hi";
        };
    }
    fn list_contains(l: List, c: UI::Component) -> bool { return false; }
    fn list_add(l: List, c: UI::Component) -> List { return List {}; }
    
    enum UI {
        struct Window {
            name: str;
            components: List;
        };
        
        enum Component {
            struct Button {
                enabled: bool;
                active: bool;
                allowAllowEvents: bool;
            };
        };
    }
    
    fn register_click_handler(window: UI::Window, btn: UI::Component::Button) {
        print("Registered click");
    }
    
    fn add_component_to_window(mut window: UI::Window, component: UI::Component) -> Result {
        if (component is UI::Component::Button) {
            let btn = component as UI::Component::Button;
            if (btn.enabled || btn.active && btn.allowAllowEvents) {
                register_click_handler(window, btn);
            }
        }
    
        if (list_contains(window.components, component)) {
            return Result::Err {};
        }
        
        window.components = list_add(window.components, component);
        return Result::Ok { };
    }
    
    fn main(args: i32) {
        create_main_window();
    
        mut let window: UI::Window = get_main_window();
        mut let component: UI::Component = create_component("Btn");
        
        mut let t: i32 = (2 + 3) * 2;
        print(t as str);
        while (t > 0) {
            t = t - 1;
            sleep(1);
        }
        
        match (add_component_to_window(window, component)) {
            Result::Err _ => {
                return;
            };
            Result::Ok w => {
                window = w.value;
            };
        }
    }
    """)

    interpreter = Interpreter()
    interpreter.visit(module)
    result = interpreter.run("main")
    #
    # assert result.value == 6
    # assert result.type_name == TypeName.parse("i32")