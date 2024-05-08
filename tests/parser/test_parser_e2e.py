from src.parser.errors import SyntaxException
from tests.parser.test_parser import create_parser


def test_parser_e2e():
    program = """
    enum UI {
        struct Window {
            name: str;
            components: List;
        };
        
        enum Component {
        
        };
    }
    
    fn add_component_to_window(mut window: UI::Window, component: UI::Component) -> Result {
        if (list_contains(window.components, component)) {
            return Result::Error {};
        };
        
        window.components = list_add(window.components, component);
        return Result::Ok { value = window; };
    }
    
    fn main(args: Sys::Args) {
        create_main_window();
    
        mut let window: UI::Window = get_main_window();
        let component: UI::Component;
        component = create_component("Btn");
        
        let t: i32 = 10;
        while (t > 0) {
            t = t - 1;
            sleep(1);
        };
        
        match (add_component_to_window(window, component)) {
            Result::Err => {
                return;
            };
            Result::Ok => {
                window = w;
            };
        };
    }
    
    """

    parser = create_parser(program, False)

    try:
        parser.parse()
    except SyntaxException as err:
        print(err, err.position)
        print(parser._token)
        raise err
