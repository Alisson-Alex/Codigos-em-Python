from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

Builder.load_string('''
<TabsLayout>:
    TabbedPanel:
        do_default_tab: False
        TabbedPanelItem:
            text: 'Tab 1'
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Content for Tab 1'
        TabbedPanelItem:
            text: 'Tab 2'
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Content for Tab 2'
''')

class TabsLayout(BoxLayout):
    pass

class TabsApp(App):
    kv_file = None  # Evita que o Kivy procure um arquivo .kv externo

    def build(self):
        return TabsLayout()
    
# Função de inicialização
def run_kivy_app():
    app = TabsApp()
    app.run()

# Chame a função para executar o aplicativo
run_kivy_app()
