from django import forms

class form_usuario(forms.Form):
    
    CHOICES = (('JuanManSantos', 'Juan Manuel Santos'),('AlvaroUribeVel', 'Alvaro Uribe Velez'),('petrogustavo','Gustavo Petro'),('mluciaramirez', 'Martha Lucia Ramirez'),('AABenedetti', 'Armando Benedetti'),('JERobledo', 'Jorgue Enrique Robledo'),('IvanCepedaCast', 'Ivan Cepeda Castro'),('piedadcordoba', 'Piedad Cordoba'),('AntanasMockus', 'Antanas Mokus'),('jcvelezuribe', 'Juan Carlos Velez Uribe'),('DanielSamperO', 'Daniel Samper Ospina'),('saludhernandezm', 'Salud Hernandez Mora'),('CristoBustos', 'Juan Fernando Cristo'),('sergio_fajardo', 'Sergio Fajardo'),('Timochenko_FARC', 'Timochenko Timoleon Jimenez '),('IvanMarquezFARC', 'Ivan Marquez'),('German_Vargas', 'German Vargas Lleras'),('ELTIEMPO', 'Periodico El Tiempo'),('ClaudiaLopez', 'Claudia Lopez Hernandez'),('RevistaSemana', 'Revista Semana'),('VickyDavilaH', 'Vicky Davila H'))
    usuario = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'onchange':'submit();'}))
