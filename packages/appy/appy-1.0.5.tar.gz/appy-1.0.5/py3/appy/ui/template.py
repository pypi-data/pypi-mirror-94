'''Base template for any UI page'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2021 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from appy.px import Px

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Template:
    '''The main UI template'''

    @classmethod
    def getPageTitle(class_, tool, o):
        '''Returns content for tag html > head > title'''
        # Return the app name in some cases
        if not o or (o == tool):
            r = tool.translate('app_name_raw')
        else:
            # The page title is based on p_o's title
            r = o.getShownValue()
        # Ensure this is a string
        r = r if isinstance(r, str) else str(r)
        # If a XHTML tag is found, keep the part before it
        if '<' in r: r = r[:r.index('<')]
        # Add p_o's page title if found
        if o and ('page' in tool.req):
            label = '%s_page_%s' % (o.class_.name, tool.req.page)
            text = tool.translate(label, blankOnError=True)
            if text:
                if r: r += ' :: '
                r += text
        return Px.truncateValue(r, width=100)

    @classmethod
    def getContentCss(class_, ctx):
        '''Return the CSS class to apply to the zone of the template that will
           host the effective page content.'''
        # In most situations, class "content" must be used. In situations where
        # a more compact design must be applied (ie, in the popup), class
        # "contentP" must be used instead.
        if ctx.popup or (not ctx.showPortlet and \
                         (ctx._px_.name in ('public', 'homes'))):
            r = 'contentP'
        else:
            r = 'content'
        return r

    # PX for which compact CSS must be used
    compactPx = {'payload': ('homes',), 'content': ('public', 'homes')}

    # CSS classes to use, for every zone and compactness
    zoneCss = {'payload': {False: 'payload', True: 'payload payloadP'},
               'content': {False: 'content', True: 'contentP'}}

    @classmethod
    def getCssFor(class_, zone, ctx):
        '''Return the CSS class(es) to apply to this p_zone'''
        # In some situations (ie, in the popup), a more compact design must be
        # applied.
        compact = ctx.popup or (not ctx.showPortlet and \
                                (ctx._px_.name in (class_.compactPx[zone])))
        return class_.zoneCss[zone][compact]

    @classmethod
    def includeLoginBox(class_, ctx):
        '''Must the login box be integrated in the current page ?'''
        # The login box has no sense if the user is already authenticated or in
        # the process of self-registering himself, or if browser incompatibility
        # has be detected.
        if not ctx.isAnon or ctx.o.isTemp() or ctx.bi: return
        # Moreover, if we are on the public page and the authentication will be
        # done by redirecting the user to tool/home, it is useless to include
        # the login box in this case, too.
        if (ctx._px_.name == 'public') and (ctx.cfg.discreetLogin == 'home'):
            return
        # Include it in any other case
        return True

    @classmethod
    def getMainStyle(class_, ctx):
        '''Return the CSS properties for the main, global zone'''
        # Get the main background image
        r = ctx.cfg.getBackground(ctx._px_, ctx, type='home')
        # Get the global height. Deduce the footer height if the footer is shown
        if ctx.showFooter:
            height = 'calc(100%% - %s)' % ctx.cfg.footerHeight
        else:
            height = '100%'
        height = 'height:%s' % height
        return '%s;%s' % (r, height) if r else height

    @classmethod
    def getPayloadStyle(class_, ctx):
        '''Gets the CSS styles to apply to the "payload" zone'''
        # The payload zone is the block portlet / content / sidebar
        # ~~~ Determine the background image
        r = ctx.cfg.getBackground(ctx._px_, ctx,
                                  type='popup' if ctx.popup else 'base')
        # ~~~ Determine the "top" property
        top = '0' if (ctx.showHeader=='sub') or (ctx.payloadCss.endswith('P')) \
                  else ctx.headerHeight
        top = 'top:%s' % top
        r = '%s;%s' % (r, top) if r else top
        return r

    @classmethod
    def getIconsStyle(class_, ctx):
        '''Get CSS styles to apply to the block of icons in the page header'''
        margin = ctx.cfg.cget('headerMargin', ctx)
        return 'margin-%s:auto' % margin

    @classmethod
    def getContent(class_, ctx):
        '''Returns the page content, with the sub-header when relevant'''
        r = '<div class="%s">%s</div>' % (class_.getCssFor('content', ctx),
                                          ctx.content(ctx, applyTemplate=False))
        # Add the sub-header when appropriate
        if ctx.showHeader == 'sub':
            r = '<div class="subbed">%s%s</div>' % (class_.pxHeader(ctx), r)
        return r

    # Hooks for defining a PX that proposes additional links or icons, before
    # and after the links/icons corresponding to top-level pages and icons.
    pxLinksBefore = pxLinks = pxLinksAfter = None

    # The global page header
    pxHeader = Px('''
     <div class="topBase"
          style=":cfg.getBackground(_px_, _ctx_, type='header')">

      <div class="top" style=":'height:%s' % headerHeight">

       <!-- Custom links (I) -->
       <x>:Template.pxLinksBefore</x>

       <!-- The burger button for collapsing the portlet -->
       <a if="showPortlet" class="burger"
          onclick="toggleCookie('appyPortlet','block','expanded',\
                'show','hide')"><img src=":url('burger.svg')" class="icon"/></a>

       <!-- Links and icons -->
       <div class="topIcons" style=":Template.getIconsStyle(_ctx_)">

        <!-- Custom links (II) -->
        <x>:Template.pxLinks</x>

        <!-- Header messages -->
        <span class="topText" var="text=cfg.getHeaderText(tool)"
              if="not popup and text">::text</span>

        <!-- The home icon -->
        <a if="not isAnon and cfg.tget('showHomeIcon', tool)"
           href=":tool.computeHomePage()">
          <img src=":url('home.svg')" class="icon"/></a>

        <!-- Connect link if discreet login -->
        <a if="isAnon and cfg.discreetLogin" id="loginIcon"
           name="loginIcon" href=":guard.getLoginUrl(_ctx_)" class="clickable">
         <img src=":url('login.svg')" class="icon"/>
         <span class="topText">:_('app_connect')</span>
        </a>

        <!-- Root pages -->
        <x if="cfg.tget('showRootPages', tool)"
           var2="pages=tool.OPage.getRoot(tool)">
         <x if="pages">:tool.OPage.pxSelector</x></x>

        <!-- Language selector -->
        <x if="ui.Language.showSelector(cfg,layout)">:ui.Language.pxSelector</x>

        <!-- User info and controls for authenticated users -->
        <x if="not isAnon" var2="logoutText=_('app_logout')">
         <!-- Config -->
         <a if="cfg.showTool(tool)" href=":'%s/view' % tool.url"
                title=":_('Tool')">
          <img src=":url('config.svg')" class="icon"/></a>
         <x if="cfg.tget('showUserLink', tool)">:user.pxUserLink</x>
         <!-- Authentication context selector -->
         <x var="ctx=config.security.authContext" if="ctx">:ctx.pxLogged</x>
         <!-- Log out -->
         <a href=":guard.getLogoutUrl(tool, user)" title=":logoutText">
          <img src=":url('logout.svg')" class="icon"/>
          <span if="cfg.logoutText">:logoutText</span></a>
        </x>

        <!-- Custom links (III) -->
        <x>:Template.pxLinksAfter</x>
       </div>

       <!-- The burger button for collapsing the sidebar -->
       <a if="showSidebar" class="burger"
          onclick="toggleCookie('appySidebar','block','expanded',\
             'show','hide')"><img src=":url('burger.svg')" class="icon"/></a>
      </div>
     </div>''',

     css='''
      .topBase { background-color:|headerBgColor|; width:100%; position:fixed;
                 color:|headerColor|; font-weight:lighter; z-index:1 }
      .top { display:flex; flex-wrap:nowrap; justify-content:space-between;
             align-items:center; margin:0 5px }
      .topIcons > a, .topIcons > select { margin:0 5px; color:|headerColor| }
      .topIcons span { text-transform: uppercase; font-weight: bold;
                       padding: 0 15px; vertical-align: -2px }
      .topText { letter-spacing:1px; padding: 0 8px }
      .burger { cursor:pointer; margin:0 5px }''')

    # The template of all base PXs
    px = Px('''
     <html var="x=handler.customInit(); cfg=config.ui; Template=ui.Template"
           dir=":dir">

      <head>
       <title>:Template.getPageTitle(tool, home)</title>
       <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
       <link rel="icon" type="image/x-icon"
             href=":url('favicon.ico', base=appName)"/>
       <link rel="apple-touch-icon" href=":url('appleicon', base=appName)"/>
       <x>::ui.Includer.getGlobal(handler, config, dir)</x>
      </head>

      <body class=":cfg.getClass('body', _px_, _ctx_)"
            var="showPortlet=ui.Portlet.show(tool, _px_, _ctx_);
                 showSidebar=ui.Sidebar.show(tool, o, layout, popup);
                 showHeader=cfg.showHeader(_px_, _ctx_, popup);
                 headerHeight=cfg.cget('headerHeight', _ctx_);
                 showFooter=cfg.showFooter(_px_, _ctx_, popup);
                 bi=ui.Browser.getIncompatibilityMessage(tool, handler)">

       <!-- Browser incompatibility message -->
       <div if="bi" class="wrongBrowser">::bi</div>

       <!-- Google Analytics stuff, if enabled -->
       <script var="gaCode=tool.getGoogleAnalyticsCode(handler, config)"
               if="gaCode">:gaCode</script>

       <!-- Popups -->
       <x>::ui.Globals.getPopups(tool, url, _, dleft, dright, popup)</x>

       <div class=":cfg.getClass('main', _px_, _ctx_)"
            style=":Template.getMainStyle(_ctx_)">

        <!-- Page header (top) -->
        <x if="showHeader == 'top'">:Template.pxHeader</x>

        <!-- Message zone -->
        <div height="0">:ui.Message.px</div>

        <!-- Login zone -->
        <x if="Template.includeLoginBox(_ctx_)">:guard.pxLogin</x>

        <!-- Payload: portlet / content / sidebar -->
        <div var="payloadCss=Template.getCssFor('payload', _ctx_)"
             class=":payloadCss" style=":Template.getPayloadStyle(_ctx_)">

         <!-- Portlet -->
         <x if="showPortlet">:ui.Portlet.px</x>

         <!-- Page content -->
         <x>::Template.getContent(_ctx_)</x>

         <!-- Sidebar -->
         <x if="showSidebar">:ui.Sidebar.px</x>
        </div>

        <!-- Cookie warning -->
        <x if="not popup and not guard.cookiesAccepted">:guard.pxWarnCookies</x>

        <!-- Footer -->
        <x if="showFooter">:ui.Footer.px</x>

       </div>
      </body>
     </html>''', prologue=Px.xhtmlPrologue)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
