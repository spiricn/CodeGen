/**
 * @file <%= headerFileName %>
 * @author Nikola Spiric <nikola.spiric.ns@gmail.com>
 */
 
#ifndef <%= headerGuard %>
#define <%= headerGuard %>

namespace wt
{

class <%= className %>{
public:
	<%= className %>();

	~<%= className %>();

private:
}; // </<%= className %>>

} // </wt>

#endif // </<%= headerGuard %>>