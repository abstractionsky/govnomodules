import flet as ft

codes = {
    1: """encoding = int(input("введи наскоко каждый битов символ кодируется: "))
a = int(input("введи наскоко меньше стало: "))
codirovka = encoding / 8
result = (a - (2 * codirovka)) / codirovka
print(result)""",
    5: """for b in range(1, 100):
    a = (6 + 1 + 1) * b + 1 + 1
    if a == 82:
        print(b)""",
    6: """def func(s, t):
    if s > 10 or t > 10:
        print("YES")
    else:
        print("NO")

spisok = "spisok = (СПИСОК)".replace(";", "-").replace("–", "-")
exec(spisok)
for s, t in spisok:
    func(s, t)""",
    10: """print(bin("ЧИСЛО")[2:])
a = int("ЧИСЛО", base=16)
b = int("ЧИСЛО", base=8)
c = int("ЧИСЛО", base=2)
print(a, b, c)"""
}

def main(page: ft.Page):
    page.title = "Abstract Project"
    page.padding = 30
    page.vertical_alignment = "center"
    def copy_code(code: int):
        page.set_clipboard(codes.get(code))
    container = ft.Row(
        spacing=30,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )
    def create_block(btn_text, *content_items):
        is_expanded = False
        
        content = ft.Column(
            controls=list(content_items),
            spacing=8,
            visible=False,
            alignment=ft.MainAxisAlignment.START
        )
        
        def toggle(e):
            nonlocal is_expanded
            is_expanded = not is_expanded
            content.visible = is_expanded
            button.text = f"{btn_text}" if is_expanded else f"{btn_text}"
            page.update()
        
        button = ft.ElevatedButton(
            text=f"{btn_text}",
            on_click=toggle,
            style=ft.ButtonStyle(
                padding=15,
                bgcolor=ft.colors.SURFACE_VARIANT,
                overlay_color=ft.colors.TRANSPARENT
            )
        )
        
        return ft.Column([button, content], spacing=8)

    block1 = create_block(
        "Задание 1",
        ft.FilledButton(
            "Скопировать код",
            icon=ft.icons.DISCOUNT,
            on_click=copy_code(1)
        ))
    block2 = create_block("Задание 5", 
        ft.FilledButton(
            "Скопировать код",
            icon=ft.icons.DISCOUNT,
            on_click=copy_code(5)
        ))
    block3 = create_block("Задание 6",
        ft.FilledButton(
            "Скопировать код",
            icon=ft.icons.DISCOUNT,
            on_click=copy_code(6)
        ))
    block4 = create_block(
        "Задание 10",
        ft.FilledButton(
            "Получить скидку", 
            icon=ft.icons.DISCOUNT,
            on_click=copy_code(10)
        )
    )
    container.controls = [block1, block2, block3, block4]
    page.add(container)

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)