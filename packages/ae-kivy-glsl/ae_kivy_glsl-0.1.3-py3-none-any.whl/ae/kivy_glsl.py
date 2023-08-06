"""
add glsl renderers/shaders to your kivy widget
==============================================

This ae namespace portion provides the mixin class :class:`ShadersMixin` that can be combined with
any Kivy widget/layout for to display GLSL-/shader-based graphics, gradients and animations.

Additionally some :ref:`built-in shaders` are integrated into this portion. More shader examples can be found in
the glsl sub-folder of the `GlslTester <https://github.com/AndiEcker/glsl_tester>`_ demo application.


usage of ShadersMixin class
---------------------------

For to add the :class:`ShadersMixin` mixin class to a Kivy widget in your python code file you have to
specify it in the declaration of your widget class. The following example is extending Kivy's
:class:`~kivy.uix.boxlayout.BoxLayout` layout with a shader::

    from kivy.uix.boxlayout import BoxLayout
    from ae.kivy_glsl import ShadersMixin

    class MyBoxLayoutWithShader(ShadersMixin, BoxLayout):


Alternatively you can declare a your shader-widget as a new kv rule within a kv file::

    <MyBoxLayoutWithShader@ShadersMixin+BoxLayout>


For to activate a shader call the :meth:`ShadersMixin.add_renderer` method::

    renderer_index = widget_instance.add_renderer()


By default :meth:`~ShadersMixin.add_renderer` is using the built-in
:data:`plasma hearts shader <plasma_hearts_shader_code>`, provided by this portion. The next example is instead using
the built-in :data:`touch wave shader <touch_wave_shader_code>`::

    from ae.kivy_glsl import touch_wave_shader_code

    widget_instance.add_renderer(shader_code=touch_wave_shader_code)


Alternatively you can use your own shader code by specifying it on call of the method :meth:`~ShadersMixin.add_renderer`
either as code block string to the `paramref:`~ShadersMixin.add_renderer.shader_code` argument or as file name to the
`paramref:`~ShadersMixin.add_renderer.shader_file` argument.

Animation shaders like the built-in touch wave and plasma hearts shaders need to be refreshed by a timer.
The refreshing frequency can be specified via the :paramref:`~ShadersMixin.add_renderer.update_freq` parameter.
For to disable the automatic creation of a timer event pass a zero value to this argument.

.. hint::
    The demo apps `ComPartY <https://gitlab.com/ae-group/comparty>`_ and
    `GlslTester <https://github.com/AndiEcker/glsl_tester>`_ are disabling the automatic timer event
    for each shader and using instead a Kivy clock timer for to update the frames of all active shaders.


Store the return value of :meth:`~ShadersMixin.add_renderer` renderer_index if you later want to deactivate the shader
with the :meth:`~ShadersMixin.del_renderer` method::

    widget_instance.del_renderer(renderer_index)


.. note::
    You can activate multiple shaders for the same widget. The visibility and intensity of each shader depends then on
    the implementation of the shader codes and the values of the input arguments (especially `alpha` and `tex_col_mix`)
    for each shader (see parameter :paramref:`~ShadersMixin.add_renderer.glsl_dyn_args`).


built-in shaders
----------------

The :data:`circled alpha shader <circled_alpha_shader_code>` is a simple gradient shader without any time-based
animations.

The :data:`touch wave shader <touch_wave_shader_code>` is animated and inspired by the kivy pulse shader example
(Danguafer/Silexars, 2010) https://github.com/kivy/kivy/blob/master/examples/shader/shadertree.py.

The animated :data:`plasma hearts shader <plasma_hearts_shader_code>` is inspired by the kivy plasma shader example
https://github.com/kivy/kivy/blob/master/examples/shader/plasma.py.

.. hint::
    The `GlslTester <https://github.com/AndiEcker/glsl_tester>`_ and `ComPartY <https://gitlab.com/ae-group/comparty>`_
    applications are demonstrating the usage of this portion.

The literals of the built-in shaders got converted into constants, following the recommendations given in the accepted
answer of `this SO question <https://stackoverflow.com/questions/20936086>`_.
"""
from functools import partial
from typing import Any, Dict, Iterable, List, Optional

from kivy.clock import Clock                                    # type: ignore
from kivy.factory import Factory                                # type: ignore
from kivy.graphics.instructions import Canvas, RenderContext    # type: ignore # pylint: disable=no-name-in-module
from kivy.graphics.vertex_instructions import Rectangle         # type: ignore # pylint: disable=no-name-in-module

from ae.base import UNSET, os_platform                          # type: ignore


__version__ = '0.1.3'


RendererType = Dict[str, Any]       #: used for to store renderer

# on some Android devices this and the touch wave shader are crashing (in vbo.so and w/o Python traceback - see also
# `this Kivy issues <https://github.com/kivy/kivy/issues/6627>`_) if the texture of the widget (or of the last shader)
# gets not fetched (w/ texture2D(texture0, tex_coord0)).
ANDROID_PATCH = '''\
  vec4 tex = texture2D(texture0, tex_coord0);
''' if os_platform == 'android' else ''''''

# --- BUILT-IN SHADERS

circled_alpha_shader_code = '''
$HEADER$

uniform float alpha;
uniform vec2 center_pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

void main(void)
{
  vec2 pix_pos = (frag_modelview_mat * gl_FragCoord).xy;
''' + ANDROID_PATCH + '''\
  float len = length(pix_pos - center_pos);
  float dis = len / max(pix_pos.x, max(pix_pos.y, max(resolution.x - pix_pos.x, resolution.y - pix_pos.y)));
  gl_FragColor = vec4(tint_ink.rgb, dis * alpha);
}
'''

touch_wave_shader_code = '''
$HEADER$

uniform float alpha;
uniform float contrast;
uniform float time;
uniform vec2 center_pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

const float TEN = 9.99999;
const float TWO = 2.00001;
const float ONE = 0.99999;

void main(void)
{
  vec2 pix_pos = (frag_modelview_mat * gl_FragCoord).xy;
''' + ANDROID_PATCH + '''\
  float len = length(pix_pos - center_pos);
  float col_comp = (sin(len / TEN - time * TEN) + ONE) / TEN;
  float dis = len / (TWO * max(resolution.x, resolution.y));
  vec4 col = tint_ink / vec4(col_comp, col_comp, col_comp, dis / (ONE / TEN + contrast)) / TEN;
  gl_FragColor = vec4(col.rgb, col.a * alpha * alpha);
}
'''

plasma_hearts_shader_code = '''
$HEADER$

uniform float alpha;
uniform float contrast;
uniform float tex_col_mix;
uniform float time;
uniform vec2 center_pos;
uniform vec2 resolution;
uniform vec4 tint_ink;

const float THOUSAND = 963.9;
const float HUNDRED = 69.3;
const float TEN = 9.9;
const float TWO = 1.83;
const float ONE = 0.99;

void main(void)
{
  vec2 pix_pos = (frag_modelview_mat * gl_FragCoord).xy;
  float x = abs(pix_pos.x - center_pos.x);
  float y = abs(pix_pos.y - center_pos.y - resolution.y);

  float m1 = x + y + cos(sin(time) * TWO) * HUNDRED + sin(x / HUNDRED) * THOUSAND;
  float m2 = y / resolution.y;
  float m3 = x / resolution.x + time * TWO;

  float c1 = abs(sin(m2 + time) / TWO + cos(m3 / TWO - m2 - m3 + time));
  float c2 = abs(sin(c1 + sin(m1 / THOUSAND + time) + sin(y / HUNDRED + time) + sin((x + y) / HUNDRED) * TWO));
  float c3 = abs(sin(c2 + cos(m2 + m3 + c2) + cos(m3) + sin(x / THOUSAND)));

  vec4 tex = texture2D(texture0, tex_coord0);
  float dis = TWO * distance(pix_pos, center_pos) / min(resolution.x, resolution.y);
  vec4 col = vec4(c1, c2, c3, contrast * (ONE - dis)) * tint_ink * TWO;
  col = mix(tex, col, tex_col_mix);
  gl_FragColor = vec4(col.rgb, col.a * sqrt(alpha));
}
'''


class ShadersMixin:
    """ shader mixin base class """
    # abstract attributes provided by the Widget instance mixed into
    canvas: Any
    center_x: float
    center_y: float
    pos: list
    size: list

    # attributes
    renderers: List[RendererType] = list()  #: list/pool of active shaders/render-contexts

    def add_renderer(self, add_to: Optional[Canvas] = None,
                     shader_code: str = plasma_hearts_shader_code, shader_file: str = "",
                     start_time: Optional[float] = 0.0, update_freq: float = 30.0,
                     **glsl_dyn_args) -> int:
        """ create new render context canvas and add it.

        :param add_to:          canvas or existing render context to add the new render context to. If not passed then
                                the canvas of the widget instance mixed-into will be used if exists. If the
                                canvas does not exist then the new render context will be set as a normal canvas.
                                By passing an already existing render context (e.g. self.renderers[-1]['render_ctx'])
                                then the new render context will be added to the passed one - in this case the new
                                render context will also get invisible if you delete the passed render context.
        :param shader_code:     fragment shader code block (will be ignored if :paramref:`.shader_file` is not empty).
        :param shader_file:     filename with the glsl shader code (with “–VERTEX” or “–FRAGMENT” sections) to load.
        :param start_time:      base/start time. Passing the default value zero is syncing the `time` glsl parameter
                                of this renderer with :meth:`kivy.clock.Clock.get_boottime()`.
                                Pass None for to initialize this argument to the current Clock boot time; this
                                way the `time` glsl argument will start by zero.
        :param update_freq:     shader/renderer update frequency. Pass 0.0 for to disable creation of an update timer.
        :param glsl_dyn_args:   extra/user dynamic shader parameters, depending on the used shader code. The keys
                                of this dict are the names of the corresponding glsl input variables in your shader
                                code. The built-in shaders (provided by this module) providing the following glsl
                                input variables:

                                * `'alpha'`: opacity (float, 0.0 - 1.0).
                                * `'center_pos'`: center position in Window coordinates (tuple(float, float)).
                                * `'contrast'`: color contrast (float, 0.0 - 1.0).
                                * `'mouse'`: mouse pointer position in Window coordinates (tuple(float, float)).
                                * `'resolution'`: width and height in Window coordinates (tuple(float, float)).
                                * `'tex_col_mix'`: factor (float, 0.0 - 1.0) for to mix the kivy input texture
                                   and the calculated color. A value of 1.0 will only show the shader color,
                                   whereas 0.0 will result in the color of the input texture (uniform texture0).
                                * `'tint_ink'`: tint color with color parts in the range 0.0 till 1.0.
                                * `'time'`: animation time (offset to :paramref:`.start_time`) in seconds. If
                                   specified as constant (non-dynamic) value then you have to call the
                                   :meth:`.next_tick` method for to increment the timer for this shader/renderer.

                                Pass a callable for to provide a dynamic/current value, which will be called on
                                each rendering frame without arguments and the return value will be passed into
                                the glsl shader.

                                .. note::
                                    Don't pass `int` values because some renderer will interpret them as `0.0`.

        :return:                index (id) of the created/added render context.
        """
        # ensure window render context
        # noinspection PyUnresolvedReferences
        import kivy.core.window     # type: ignore # noqa: F401 # pylint: disable=unused-import, import-outside-toplevel

        if start_time is None:
            start_time = Clock.get_boottime()
        if 'center_pos' not in glsl_dyn_args:
            glsl_dyn_args['center_pos'] = lambda: (self.center_x, self.center_y)
        if 'tint_ink' not in glsl_dyn_args:
            glsl_dyn_args['tint_ink'] = (0.546, 0.546, 0.546, 1.0)    # colors * shader_code.TWO ~= (1.0, 1.0, 1.0)

        ren_ctx = RenderContext(use_parent_modelview=True, use_parent_projection=True, use_parent_frag_modelview=True)
        with ren_ctx:
            rectangle = Rectangle(pos=self.pos, size=self.size)

        shader = ren_ctx.shader
        try:
            if shader_file:
                old_value = shader.source
                shader.source = shader_file
            else:
                old_value = shader.fs
                shader.fs = shader_code
            fail_reason = "" if shader.success else "shader.success is False"
        except Exception as ex:
            fail_reason = f"exception {ex}"
            old_value = UNSET
        if fail_reason:
            if old_value is not UNSET:
                if shader_file:
                    shader.source = old_value
                else:
                    shader.fs = old_value
            raise ValueError(f"ShadersMixin.add_renderer: shader compilation failed:{fail_reason} (see console output)")

        renderer_idx = len(self.renderers)
        if renderer_idx == 0:
            self.renderers = list()     # create attribute on this instance (leave class attribute untouched emtpy list)

        if add_to is None and self.canvas is not None:
            add_to = self.canvas
        if add_to is None:
            self.canvas = ren_ctx
        else:
            add_to.add(ren_ctx)

        renderer = dict(added_to=add_to, deleted=False, render_ctx=ren_ctx, rectangle=rectangle,
                        shader_code=shader_code, shader_file=shader_file,
                        start_time=start_time, update_freq=update_freq, glsl_dyn_args=glsl_dyn_args)
        self.renderers.append(renderer)

        if update_freq:
            renderer['timer'] = Clock.schedule_interval(partial(self._refresh_glsl, renderer_idx), 1 / update_freq)

        return renderer_idx

    def del_renderer(self, renderer_idx: int):
        """ remove renderer added via add_renderer.

        :param renderer_idx:    index of the renderer to remove (returned by :meth:`.add_renderer`). If the passed
                                index value is less then zero then :attr:`~ShadersMixin.renderers` left untouched.
        """
        if renderer_idx < 0 or not self.renderers or renderer_idx >= len(self.renderers):
            return              # ignore if app disabled rendering for too slow devices or on duplicate render deletion

        renderer = self.renderers[renderer_idx]
        renderer['deleted'] = True
        self.reset_timers(remove_deleted=True)
        if renderer_idx == len(self.renderers) - 1:
            renderer = self.renderers.pop(renderer_idx)
            while self.renderers and self.renderers[-1]['deleted']:
                self.renderers.pop(-1)

        added_to = renderer['added_to']
        if added_to:
            added_to.remove(renderer['render_ctx'])
        else:
            self.canvas = None

    def next_tick(self, increment: float = 1 / 30.):
        """ increment glsl `time` input argument if renderers get updated manually/explicitly by the app.

        :param increment:       delta in seconds for the next refresh of all renderers with a `time` constant.
        """
        for renderer in self.renderers:
            if not renderer['deleted']:
                dyn_args = renderer['glsl_dyn_args']
                if 'time' in dyn_args and not callable(dyn_args['time']):
                    dyn_args['time'] += increment

    def on_pos(self, _instance: Any, value: Iterable):
        """ pos """
        for ren in self.renderers:
            if not ren['deleted']:
                ren['rectangle'].pos = value

    def on_size(self, _instance: Any, value: Iterable):
        """ size changed """
        for ren in self.renderers:
            if not ren['deleted']:
                ren['rectangle'].size = value

    def _refresh_glsl(self, renderer_idx: int, _dt: float):
        """ timer/clock event handler for to animate and sync one canvas shader. """
        self.refresh_renderer(self.renderers[renderer_idx])

    def refresh_renderer(self, renderer: RendererType):
        """ update the shader arguments for the current animation frame.

        :param renderer:        dict with render context, rectangle and glsl input arguments.
        """
        ren_ctx = renderer['render_ctx']
        start_time = renderer['start_time']
        if callable(start_time):
            start_time = start_time()

        # first set the defaults for glsl fragment shader input args (uniforms)
        glsl_kwargs = renderer['glsl_dyn_args']
        ren_ctx['alpha'] = 0.99
        ren_ctx['contrast'] = 0.69
        ren_ctx['resolution'] = list(map(float, self.size))
        ren_ctx['tex_col_mix'] = 0.69
        if not callable(glsl_kwargs.get('time')):
            ren_ctx['time'] = Clock.get_boottime() - start_time

        # .. then overwrite glsl arguments with dynamic user values
        for key, val in glsl_kwargs.items():
            ren_ctx[key] = val() if callable(val) else val

    def refresh_renderers(self):
        """ manually update all renderers. """
        for renderer in self.renderers:
            self.refresh_renderer(renderer)

    def reset_timers(self, remove_deleted: bool = False):
        """ unschedule (if created) and reschedule (if only_remove_deleted=False) active timers of this instance.

        :param remove_deleted:  pass True to only remove deleted times (all active shaders will keep their old timer).
        """
        for idx, renderer in enumerate(self.renderers):
            update_freq = renderer['update_freq']
            deleted = renderer['deleted']
            if update_freq and 'timer' in renderer and (deleted or not remove_deleted):
                Clock.unschedule(renderer['timer'])
                if not deleted:
                    renderer['timer'] = Clock.schedule_interval(partial(self._refresh_glsl, idx), 1 / update_freq)


Factory.register('ShadersMixin', cls=ShadersMixin)
